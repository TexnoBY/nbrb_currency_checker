import zlib
from datetime import datetime, timedelta

import httpx
from fastapi import FastAPI, HTTPException
from sqlalchemy import and_

from database_helper.database_connection import DatabaseConnection
from database_helper.models import Base, Rate, Currency
from utils.logger import base_logger, error_logger, debug_logger

app = FastAPI()

DATABASE_URL = 'sqlite:///./exchange_rates.db'
db_connection = DatabaseConnection(DATABASE_URL)


# Endpoint 1
@app.get('/load_exchange_rates/')
async def load_exchange_rates(date: str):
    try:
        rate_response = httpx.get('https://api.nbrb.by/exrates/rates',
                                  params={
                                      'ondate': date,
                                      'periodicity': 0
                                  })

        session = db_connection.get_session()
        for rate in [Rate(**item) for item in rate_response.json()]:
            session.add(rate)
        session.commit()
        base_logger.info(f'exchange rates for {date} loaded successfully from https://api.nbrb.by/exrates/rates')
        session.close()

        response = {'message': f'Data for {date} loaded successfully'}
        crc = zlib.crc32(str(response).encode())
        return response, {'CRC32': crc}

    except Exception as ex:
        error_logger.exception(ex.__str__())
        return ex.__str__()


# Endpoint 2
@app.get('/exchange_rate/')
async def get_exchange_rate(date: str, cur_id: str):
    session = db_connection.get_session()
    date = datetime.strptime(date, '%Y-%m-%d')
    exchange_rate = session.query(Rate).filter(and_(Rate.date == date.__str__().replace(' ', 'T'),
                                                    Rate.cur_id == int(cur_id))).first()
    if exchange_rate:
        debug_logger.debug(
            f'get exchange_rate for currency: {exchange_rate.cur_name}, with rate: {exchange_rate.cur_official_rate}'
        )
    else:
        debug_logger.info('Exchange rate not found')
        raise HTTPException(status_code=404, detail='Exchange rate not found')

    shift = timedelta(max(1, (date.weekday() + 6) % 7 - 3))
    previous_work_day = date - shift

    exchange_rate_prev = session.query(Rate).filter(and_(Rate.date == previous_work_day.__str__().replace(' ', 'T'),
                                                         Rate.cur_id == cur_id)).first()

    rate_diff_str = ''
    if exchange_rate_prev:
        rate_diff = exchange_rate_prev.cur_official_rate - exchange_rate.cur_official_rate
        if rate_diff >= 0:
            rate_diff_str = '+' + str(rate_diff)
        else:
            rate_diff_str = str(rate_diff)
        debug_logger.debug(
            f'get exchange_rate for previous day for currency: {exchange_rate_prev.cur_name}, with rate: {exchange_rate_prev.cur_official_rate}'
        )

    response = {
        'message': f'Exchange rate for {date} is {exchange_rate.cur_official_rate}{rate_diff_str} for {exchange_rate.cur_scale} {exchange_rate.cur_abbreviation}'
    }
    crc = zlib.crc32(str(response).encode())

    return response, {'CRC32': crc}


@app.on_event('startup')
async def startup_event():
    try:
        session = db_connection.get_session()

        currency_response = httpx.get('https://api.nbrb.by/exrates/currencies')
        for currency in [Currency(**item) for item in currency_response.json()]:
            if session.get(Currency, currency.cur_id):
                session.merge(currency)
            else:
                session.add(currency)
        session.commit()

        base_logger.info('update currency information from https://api.nbrb.by/exrates/currencies')

        session.close()

    except Exception as ex:
        error_logger.exception(ex.__str__())


if __name__ == '__main__':
    import uvicorn

    db_connection.connect()
    Base.metadata.create_all(bind=db_connection.get_engine())

    debug_logger.debug('server runs')
    uvicorn.run(app, host="0.0.0.0", port=8000)
