import os

from dotenv import load_dotenv

load_dotenv()

DEVS = [ 6952656422, 6314633791]

KYNAN = list(
    map(
        int,
        os.getenv(
            "KYNAN",
            "6952656422 6314633791",
        ).split(),
    )
)

API_ID = int(os.getenv("API_ID", "27523718"))

API_HASH = os.getenv("API_HASH", "5fb07188233692a8fdfe5c084e04fc50")

BOT_TOKEN = os.getenv("BOT_TOKEN", "7107005038:AAFxWKm1WwlhmaExpYx1HKd8HIgrN1ghOMM")

OWNER_ID = int(os.getenv("OWNER_ID", "6952656422"))

USER_ID = list(
    map(
        int,
        os.getenv(
            "USER_ID",
            "6952656422 6314633791",
        ).split(),
    )
)

LOG_UBOT = int(os.getenv("LOG_UBOT", "-1002193703074"))

LOG_SELLER = int(os.getenv("LOG_SELLER", "-1004282420800"))

BLACKLIST_CHAT = list(
    map(
        int,
        os.getenv(
            "BLACKLIST_CHAT",
            "-1001951905494 -1001794660377",
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
    "mongodb+srv://satria:17nov2003@cluster0.zgpca1t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)

DB_NAME = os.getenv("DB_NAME", "emenubot")
