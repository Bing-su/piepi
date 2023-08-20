from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Literal
from zipfile import ZipFile

from ninja import Field, File, Form, Router, Schema, UploadedFile
from ninja.errors import HttpError
from pydantic import Extra, constr

from .models import Package

router = Router()

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


def normalize(name: str) -> str:
    return re.sub(r"[-_\.]+", "-", name).lower()


def get_sha256(content: UploadedFile, metadata: Metadata) -> str:
    if metadata.sha256_digest:
        return metadata.sha256_digest

    sha256 = hashlib.sha256()
    for chunk in content.chunks():
        sha256.update(chunk)
    content.seek(0)
    return sha256.hexdigest()


def get_metadata(content: UploadedFile) -> bytes:
    data = b""
    if content.name.endswith(".tar.gz"):
        return data
    with ZipFile(content) as zipfile:
        for info in zipfile.infolist():
            if Path(info.filename).name == "METADATA":
                data = zipfile.read(info.filename)
                break
    content.seek(0)
    return data


@router.post("/")
def upload(request, content: UploadedFile = File(...), metadata: Metadata = Form(...)):
    if not content.name.endswith((".tar.gz", ".whl")):
        msg = "Only '.tar.gz' and '.whl' files are supported."
        raise HttpError(400, msg)

    if Package.objects.filter(filename=content.name).exists():
        msg = f"Package with this name({content.name}) already exists."
        raise HttpError(400, msg)

    package = Package(
        name=normalize(metadata.name),
        file=content,
        filename=content.name,
        sha256=get_sha256(content, metadata),
        metadata=get_metadata(content),
        requires_python=metadata.requires_python,
    )
    package.save()
    return package.file.url
