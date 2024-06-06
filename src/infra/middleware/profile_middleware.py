from typing import Callable

from fastapi import Request
from pyinstrument import Profiler
from pyinstrument.renderers.html import HTMLRenderer
from pyinstrument.renderers.speedscope import SpeedscopeRenderer
from starlette.middleware.base import BaseHTTPMiddleware

from src.infra.config import settings


class ProfileMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        if not settings.PROFILE or not request.query_params.get("profile", False):
            return await call_next(request)

        profile_tipo_renderizacao = {
            "html": HTMLRenderer,
            "speedscope": SpeedscopeRenderer,
        }

        profile_tipo = request.query_params.get("profile_format", "html")
        with Profiler(interval=0.001) as profiler:
            response = await call_next(request)

        tipo_extensao = {"html": "html", "speedscope": "speedscope.json"}
        extension = tipo_extensao[profile_tipo]
        render = profile_tipo_renderizacao[profile_tipo]()
        with open(f"profile.{extension}", "w") as out:
            out.write(profiler.output(renderer=render))
        return response
