import yaml


class Config:
    def __init__(self, filepath):
        with open(filepath) as f:
            parsed = yaml.full_load(f).get("config")
        self.DATABASE_CONNECTION: str = parsed.get("database_connection")
        self.JWT_SECRET_KEY: str = parsed.get(
            "jwt_secret_key", parsed.get("secret_key")
        )
        self.JWT_ALGORITHM: str = parsed.get("jwt_algorithm", "HS256")
        self.JWT_EXPIRE_MINUTES: int = int(parsed.get("jwt_expire_minutes", 600))
        self.FAST_API_SECRET_KEY: str = parsed.get(
            "fast_api_secret_key", parsed.get("secret_key")
        )
