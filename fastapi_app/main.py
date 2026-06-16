from fastapi import FastAPI
from fastapi_app.routes.auth_router import api_router
from fastapi_app.routes.data_integration import router as data_integration_router
from fastapi_app.routes.data_processing import router as data_processing_router
from fastapi_app.routes.forecast import router as forecast_router
from fastapi_app.routes.recommendation import router as recommendation_router
from fastapi_app.routes.data_sources import router as data_sources_router
from fastapi_app.routes.uploads import router as uploads_router
from fastapi_app.routes.validation import router as validation_router
from fastapi_app.routes.processing import router as processing_router
from fastapi_app.routes.forecast_engine import router as forecast_engine_router
from fastapi_app.db.session import init_db
# Import models so they are registered with SQLAlchemy before init_db()
from fastapi_app.models.auth_model import User  # noqa: F401
from fastapi_app.models.data_source_model import DataSource  # noqa: F401
from fastapi_app.models.upload_model import Upload  # noqa: F401
from fastapi_app.models.validation_error_model import ValidationError  # noqa: F401

app = FastAPI(title='Demand Forecasting Backend')

# Initialize database on startup
init_db()

app.include_router(api_router)
app.include_router(data_integration_router)
app.include_router(data_processing_router)
app.include_router(forecast_router)
app.include_router(recommendation_router)
app.include_router(data_sources_router)
app.include_router(uploads_router)
app.include_router(validation_router)
app.include_router(processing_router)
app.include_router(forecast_engine_router)
