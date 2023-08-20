import orjson
from ninja import NinjaAPI
from ninja.parser import Parser
from ninja.renderers import BaseRenderer
from ninja.types import DictStrAny
from pydantic import BaseModel

from server.main import router


class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        if isinstance(data, BaseModel):
            data = data.model_dump()
        return orjson.dumps(data)


class ORJSONParser(Parser):
    def parse_body(self, request) -> DictStrAny:
        return orjson.loads(request.body)


api = NinjaAPI(renderer=ORJSONRenderer(), parser=ORJSONParser())
api.add_router("", router)
