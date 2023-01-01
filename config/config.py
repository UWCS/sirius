import yaml


class Config:
    def __init__(self, filepath):
        with open(filepath) as f:
            parsed = yaml.full_load(f).get("config")
        self.DATABASE_CONNECTION = parsed.get("database_connection")
