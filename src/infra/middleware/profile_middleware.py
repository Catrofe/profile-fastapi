from typing import Callable

from fastapi import Request
from pyinstrument import Profiler
from pyinstrument.renderers.html import HTMLRenderer
from pyinstrument.renderers.speedscope import SpeedscopeRenderer
from starlette.middleware.base import BaseHTTPMiddleware


class ProfileMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        if app_config.profile:
            """Profile the current request
            Taken from https://pyinstrument.readthedocs.io/en/latest/guide.html#profile-a-web-request-in-fastapi
            with small improvements.
            """
            profile_type_to_renderer = {
                "html": HTMLRenderer,
                "speedscope": SpeedscopeRenderer,
            }

            if request.query_params.get("profile", False):
                profile_type = request.query_params.get("profile_format", "html")
                with Profiler(interval=0.001, async_mode="enabled") as profiler:
                    response = await call_next(request)

                profile_type_to_ext = {"html": "html", "speedscope": "speedscope.json"}
                extension = profile_type_to_ext[profile_type]
                renderer = profile_type_to_renderer[profile_type]()
                with open(f"profile.{extension}", "w") as out:
                    out.write(profiler.output(renderer=renderer))
                return response
        return await call_next(request)


