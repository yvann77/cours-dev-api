from sqlalchemy import TIMESTAMP, Column ,Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Class de base pour créer les models
Base= declarative_base()

class Teams (Base):
    __tablename__ = "team"
    teamid=Column(Integer,primary_key = True, nullable = False)
    teamname = Column(String, nullable=False)
    league = Column(String, nullable=False)
    country = Column(String, nullable=False)
    championleague = Column(Boolean, nullable=True, server_default= 'TRUE')
    chapeau = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')