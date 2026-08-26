import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import src.models.models

from src.core.config import settings
from src.core.errors.handlers import register_error_handlers
from src.routes.routes import api_router

logging.basicConfig(
    level=logging.DEBUG if settings.PROFILE == "dev" else logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    root_path=settings.PREFIX_ROUTER,
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://frontend:4200", 
        "http://localhost:4200",
        settings.FRONTEND_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request):
    root_path = request.scope.get("root_path", "").rstrip("/")
    return get_swagger_ui_html(
        openapi_url=f"{root_path}{app.openapi_url}",
        title=f"{app.title} - Swagger UI",
        swagger_js_url=f"{root_path}/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url=f"{root_path}/static/swagger-ui/swagger-ui.css",
        swagger_favicon_url=f"{root_path}/static/swagger-ui/favicon-32x32.png",
    )


@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url="/static/redoc/redoc.standalone.js",
    )


register_error_handlers(app)

app.include_router(api_router)
