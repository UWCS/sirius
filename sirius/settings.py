from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret_key: str = "secret_key"
    jwt_algorithm: str = "HS256"
    jwt_expire_mins: int = 600
    fastapi_secret_key: str = "secrey_key"
    ldap_url: str = "localhost"
    ldap_user: str = "cn=admin,dc=internal,dc=uwcs,dc=co,dc=uk"
    ldap_password: str

    class Config:
        env_file = ".env"  # load from a .env file
        env_prefix = "SIRIUS_"  # env vars are prefixed with SIRIUS_
