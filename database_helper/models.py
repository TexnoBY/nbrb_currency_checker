from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Currency(Base):
    __tablename__ = "currency"
    cur_id = Column(Integer, primary_key=True, index=True, name='Cur_ID')
    cur_parent_id = Column(Integer, name='Cur_ParentID')
    cur_code = Column(String, name='Cur_Code')
    cur_abbreviation = Column(String, name='Cur_Abbreviation')
    cur_name = Column(String, name='Cur_Name')
    cur_name_bel = Column(String, name='Cur_Name_Bel')
    cur_name_eng = Column(String, name='Cur_Name_Eng')
    cur_quot_name = Column(String, name='Cur_QuotName')
    cur_quot_name_bel = Column(String, name='Cur_QuotName_Bel')
    cur_quot_name_eng = Column(String, name='Cur_QuotName_Eng')
    cur_name_multi = Column(String, name='Cur_NameMulti')
    cur_name_bel_multi = Column(String, name='Cur_Name_BelMulti')
    cur_name_eng_multi = Column(String, name='Cur_Name_EngMulti')
    cur_scale = Column(Integer, name='Cur_Scale')
    cur_periodicity = Column(Integer, name='Cur_Periodicity')
    cur_date_start = Column(String, name='Cur_DateStart')
    cur_date_end = Column(String, name='Cur_DateEnd')

    def __init__(self,
                 Cur_ID,
                 Cur_ParentID,
                 Cur_Code,
                 Cur_Abbreviation,
                 Cur_Name,
                 Cur_Name_Bel,
                 Cur_Name_Eng,
                 Cur_QuotName,
                 Cur_QuotName_Bel,
                 Cur_QuotName_Eng,
                 Cur_NameMulti,
                 Cur_Name_BelMulti,
                 Cur_Name_EngMulti,
                 Cur_Scale,
                 Cur_Periodicity,
                 Cur_DateStart,
                 Cur_DateEnd,
                 ):
        self.cur_id = Cur_ID
        self.cur_parent_id = Cur_ParentID
        self.cur_code = Cur_Code
        self.cur_abbreviation = Cur_Abbreviation
        self.cur_name = Cur_Name
        self.cur_name_bel = Cur_Name_Bel
        self.cur_name_eng = Cur_Name_Eng
        self.cur_quot_name = Cur_QuotName
        self.cur_quot_name_bel = Cur_QuotName_Bel
        self.cur_quot_name_eng = Cur_QuotName_Eng
        self.cur_name_multi = Cur_NameMulti
        self.cur_name_bel_multi = Cur_Name_BelMulti
        self.cur_name_eng_multi = Cur_Name_EngMulti
        self.cur_scale = Cur_Scale
        self.cur_periodicity = Cur_Periodicity
        self.cur_date_start = Cur_DateStart
        self.cur_date_end = Cur_DateEnd


class Rate(Base):
    __tablename__ = "rate"
    rate_id = Column(Integer, primary_key=True, name='Rate_ID', autoincrement=True)
    cur_id = Column(Integer, ForeignKey(Currency.cur_id), name='Cur_ID')
    date = Column(String, name='Date')
    cur_abbreviation = Column(String, ForeignKey(Currency.cur_abbreviation), name='Cur_Abbreviation')
    cur_scale = Column(Integer, ForeignKey(Currency.cur_scale), name='Cur_Scale')
    cur_name = Column(String, ForeignKey(Currency.cur_name), name='Cur_Name')
    cur_official_rate = Column(Float, name='Cur_OfficialRate')

    def __init__(self,
                 Cur_ID,
                 Date,
                 Cur_Abbreviation,
                 Cur_Scale,
                 Cur_Name,
                 Cur_OfficialRate):
        self.cur_id = Cur_ID
        self.date = Date
        self.cur_abbreviation = Cur_Abbreviation
        self.cur_scale = Cur_Scale
        self.cur_name = Cur_Name
        self.cur_official_rate = Cur_OfficialRate
