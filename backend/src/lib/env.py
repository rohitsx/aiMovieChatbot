from dotenv import dotenv_values

env = dotenv_values(".env")
config = dict(env)
