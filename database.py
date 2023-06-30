from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://yvann_render:IDpYil4X9K3VWiF1oyzAXwB1cFQj8pvp@dpg-ci8rn35gkuvmfnsaactg-a.frankfurt-postgres.render.com/football_render'
# equivalent à un connect
database_engine = create_engine(DATABASE_URL)
# equivalent à un cursor
SessionTemplate = sessionmaker(bind=database_engine, autocommit=False, autoflush=False)



def get_cursor():
    db= SessionTemplate()
    try : 
        yield db
    finally : 
        db.close()