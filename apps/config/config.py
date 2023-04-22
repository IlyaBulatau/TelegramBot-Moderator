from environs import Env

env = Env()
env.read_env()

TOKEN=env("TOKEN")
DB_LOGIN=env("DB_LOGIN")
DB_PASSWORD=env("DB_PASSWORD")