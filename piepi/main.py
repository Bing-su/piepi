from __future__ import annotations

from typing import Any, Literal

from ninja import Field, File, Form, NinjaAPI, Schema, UploadedFile
from pydantic import Extra, constr

api = NinjaAPI()

name_regex = r"(?i)^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$"


class Metadata(Schema, extra=Extra.allow):
    name: constr(pattern=name_regex)
    version: str
    metadata_version: str
    dynamic: list[str] = Field(default_factory=list)
    platform: list[str] = Field(default_factory=list)
    supported_platform: str = ""
    summary: str = ""
    description: str = ""
    description_content_type: str = ""
    keywords: str = ""
    home_page: str = ""
    download_url: str = ""
    author: str = ""
    author_email: str = ""
    maintainer: str = ""
    maintainer_email: str = ""
    license: str = ""  # noqa: A003
    classifier: list[str] = Field(default_factory=list)
    requires_dist: list[str] = Field(default_factory=list)
    requires_python: str = ""
    requires_external: str = ""
    project_url: list[str] = Field(default_factory=list)
    provides_extra: list[str] = Field(default_factory=list)
    provides_dist: list[str] = Field(default_factory=list)
    obsoletes_dist: list[str] = Field(default_factory=list)

    action: Literal["file_upload"] = Field(..., alias=":action")
    protocol_version: Literal["1"]
    sha256_digest: str = ""
    md5_digest: str = ""
    blake2_256_digest: str = ""
    filetype: Literal["bdist_wheel", "sdist"]
    pyversion: str = ""


@api.get("/")
async def index(request, data: Any = "Hello, World!"):
    print(repr(data))
    return repr(data)


@api.post("/")
async def upload(
    request, content: UploadedFile = File(...), metadata: Metadata = Form(...)
):
    print(metadata)

    print(content.name)

    return repr(request.POST)
