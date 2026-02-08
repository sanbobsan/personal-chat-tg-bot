from decouple import config  # type: ignore


class Config:
    TOKEN: str = config("TOKEN")
    ADMIN: int = int(config("ADMIN"))


config = Config
