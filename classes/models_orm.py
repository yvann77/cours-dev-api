from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base


# Class de base pour créer les models
Base= declarative_base()

class Teams (Base):
    __tablename__ = "team"
    teamid=Column(Integer,primary_key = True, nullable = False)
    teamname = Column(String, nullable=False)
    league = Column(String, nullable=False)
    marketvalue = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')


class Transfers(Base):
    __tablename__="transfer"
    transferid = Column(Integer, primary_key=True, nullable=False)
    playername = Column(String, nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    transferat = Column(String, nullable=False)
    teamid = Column(String, ForeignKey("team.teamid", ondelete="RESTRICT"), nullable=False)  # Les Foreign Keys sont basés sur les clé principales des autres tables mais ce n'est pas obligatoire
    transferprice = Column(String, nullable=False)
    created_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')

class Expenses(Base):
    __tablename__="expense"
    expensesid= Column(Integer, primary_key=True, nullable=False)
    teamid= Column(Integer, ForeignKey("team.teamid", ondelete="RESTRICT"), nullable=False)
    teamname= Column(Integer, ForeignKey("team.teamname", ondelete="RESTRICT"), nullable=False)  # Les Foreign Keys sont basés sur les clé principales des autres tables mais ce n'est pas obligatoire
    arrivalsnumber = Column(Integer, nullable=False)
    teamexpenses = Column(String, nullable=False)
    revenues = Column(String, nullable=False)
    balance = Column(String, nullable=False)
    expenses_date=Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")