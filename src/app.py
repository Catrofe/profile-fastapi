from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import logging
from src.router.router_transaction import router




def criar_app() -> FastAPI:
    logging.info("-> Criando aplicação")
    app = FastAPI(
        title="profile-fastapi",
        openapi_url="/v2/api-docs",
        redoc_url=None,
    )

    logging.info("-> Adicionando rotas")
    adicionar_rotas(app)

    return app


def adicionar_rotas(app: FastAPI) -> None:
    app.include_router(router, default_response_class=ORJSONResponse)


def adicionar_handlers(app: FastAPI) -> None:
    ...


def adicionar_middlewares(app: FastAPI) -> None:
    ...


def adicionando_eventos(app: FastAPI) -> None:
    ...