import os

class Config:
    API_ID = int(os.getenv("API_ID", "22135296"))
    API_HASH = os.getenv("API_HASH", "b3051c4c2dfe4ef65f7146d172d3ddaf")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7824487725:AAFuc-5yS3CsEHT5CQ-OVFIVny9iYlbR22o")
