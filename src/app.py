import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from infra import eventos
from infra.middleware.profile_middleware import ProfileMiddleware
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

    logging.info("-> Adicionando middlewares")
    adicionar_middlewares(app)

    logging.info("-> Adicionando eventos")
    adicionando_eventos(app)

    return app


def adicionar_rotas(app: FastAPI) -> None:
    app.include_router(
        router, prefix="/transaction", default_response_class=ORJSONResponse
    )


# def adicionar_handlers(app: FastAPI) -> None: ...


def adicionar_middlewares(app: FastAPI) -> None:
    app.add_middleware(ProfileMiddleware)


def adicionando_eventos(app: FastAPI) -> None:
    app.add_event_handler("startup", eventos.preparar_aplicacao)
    app.add_event_handler("shutdown", eventos.encerrar_aplicacao)
