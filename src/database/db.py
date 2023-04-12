import configparser
import pathlib

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

file_config = pathlib.Path(__file__).parent.parent.joinpath('conf/config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DEV_DB', 'USER')
password = config.get('DEV_DB', 'PASSWORD')
db_name = config.get('DEV_DB', 'DB_NAME')
domain = config.get('DEV_DB', 'DOMAIN')
port = config.get('DEV_DB', 'PORT')

URI = f"postgresql+psycopg2://{username}:{password}@{domain}:{port}/{db_name}"
engine = create_engine(URI, echo=True)

DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = DBSession()
    try:
        yield db
    # except SQLAlchemyError as err:
    #     db.rollback()
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()
