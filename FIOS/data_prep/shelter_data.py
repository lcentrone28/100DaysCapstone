from dotenv import load_dotenv
import os

load_dotenv()

SHELTER_APP_TOKEN= os.getenv("SHELTER_APP_TOKEN")

API_ENDPOINT = os.getenv("SHELTER_API_ENDPOINT")