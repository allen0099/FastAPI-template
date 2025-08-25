"""
Modified source: https://github.com/priyanshu-panwar/fastapi-utilities/blob/master/fastapi_utilities/timer/middleware.py
"""

import time
from logging import Logger
from logging import getLogger

from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from starlette.middleware.base import RequestResponseEndpoint


def add_timer_middleware(
    app: FastAPI,
    show_avg: bool = False,
    reset_after: int = 100000,
    logger: Logger = getLogger("timer"),
) -> None:
    request_counter = 0
    total_response_time = 0.0

    @app.middleware("http")
    async def timer_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
        nonlocal request_counter, total_response_time

        start_time = time.time()
        response: Response = await call_next(request)
        process_time = (time.time() - start_time) * 1000

        if request.method == "OPTIONS":
            return response

        logger.debug('::  Time Taken  :: %010.2f ms "%s - %s"', process_time, request.method, request.url.path)
        response.headers["X-Process-Time"] = str(process_time)

        if show_avg:
            request_counter += 1
            total_response_time += process_time
            average_response_time = total_response_time / request_counter if request_counter > 0 else 0
            logger.debug(":: Average Time :: %010.2f ms", average_response_time)

            if request_counter % reset_after == 0:
                request_counter = 0
                total_response_time = 0.0

        return response
