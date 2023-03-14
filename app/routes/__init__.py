from typing import Any

from fastapi import APIRouter

from . import user

_route_list: list[Any] = [user]

routes: APIRouter = APIRouter()

for route in _route_list:
    if hasattr(route, "router"):
        routes.include_router(route.router)

    else:
        raise AttributeError(f"Route {route} does not have router attribute.")
