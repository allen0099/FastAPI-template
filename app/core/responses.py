from collections.abc import Callable
from collections.abc import Mapping
from decimal import Decimal
from logging import Logger
from logging import getLogger
from typing import Any

import orjson
from arrow import Arrow
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.background import BackgroundTask

logger: Logger = getLogger(__name__)


def _default(obj: Any) -> Any:
    logger.debug("Orjson converter: %s", type(obj))

    if isinstance(obj, BaseModel):
        return obj.model_dump()

    if isinstance(obj, Decimal):
        return float(obj)

    if isinstance(obj, Arrow):
        return obj.isoformat()

    if isinstance(obj, bytes):
        return obj.decode()

    raise TypeError


class ORJSONResponse(JSONResponse):
    # Override the default JSONResponse to use orjson
    # same from fastapi.responses.ORJSONResponse

    def __init__(
        self,
        content: Any,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
        # Customized default to use orjson
        default: Callable[[Any], Any] = _default,
    ) -> None:
        self.default = default

        super().__init__(content, status_code, headers, media_type, background)

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY, default=self.default)
