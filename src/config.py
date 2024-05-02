import os
from dataclasses import dataclass

@dataclass
class DBConfig:
    URI = os.environ.get("MONGODB_URI")
    NAME = os.environ.get("MONGODB_NAME")

@dataclass
class DBCollections:
    USER_LOG = "user_log"
    USER_COOKIES = "user-cookies"
    USER_LOGIN = "user_login"