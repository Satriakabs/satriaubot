import os

from dotenv import load_dotenv

load_dotenv()

DEVS = [ 6470638277
]

KYNAN = list(
    map(
        int,
        os.getenv(
            "KYNAN",
            "6470638277",
        ).split(),
    )
)

API_ID = int(os.getenv("API_ID", "25001166"))

API_HASH = os.getenv("API_HASH", "1a7f9d7df73031e9e6d88ac97f87b374")

BOT_TOKEN = os.getenv("BOT_TOKEN", "7111516792:AAGbW5yIBifKcv5PEWNgOoeHBcfQTfIsUVM")

OWNER_ID = int(os.getenv("OWNER_ID", "6470638277"))

USER_ID = list(
    map(
        int,
        os.getenv(
            "USER_ID",
            "6470638277",
        ).split(),
    )
)

LOG_UBOT = int(os.getenv("LOG_UBOT", "-1002097059025"))

LOG_SELLER = int(os.getenv("LOG_SELLER", "-1002097059025"))

BLACKLIST_CHAT = list(
    map(
        int,
        os.getenv(
            "BLACKLIST_CHAT",
            "-1002052076988",
        ).split(),
    )
)

MAX_BOT = int(os.getenv("MAX_BOT", "30"))

RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")

OPENAI_KEY = os.getenv(
    "OPENAI_KEY",
    "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",
).split()

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://TerbaikXD:Faizal123Fajar@cluster0.hxzytme.mongodb.net/TerbaikXD?retryWrites=true&w=majority&appName=Cluster0",
)

DB_NAME = os.getenv("DB_NAME", "satriaubot")
