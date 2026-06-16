import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL = os.getenv(
#      "DATABASE_URL",
#      "mysql+pymysql://root:password@localhost:3306/ai_demand_forecast"
# )
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "change_this_secret_in_production"
)

JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

DEFAULT_DATASET_PATH = os.getenv(
    "DEFAULT_DATASET_PATH",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "demand forecasting dataset.csv"))
)

ACCESS_TOKEN_EXPIRE = timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
)