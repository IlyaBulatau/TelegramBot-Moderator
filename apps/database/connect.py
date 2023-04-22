from sqlalchemy import create_engine

from apps.database.models import Base
from apps.config.config import DB_LOGIN, DB_PASSWORD

engine = create_engine(url=f'postgresql+psycopg2://{DB_LOGIN}:{DB_PASSWORD}@localhost/TeleBotModerator', echo=True)
engine.connect()

Base.metadata.create_all(engine)