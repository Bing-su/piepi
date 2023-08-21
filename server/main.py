from __future__ import annotations

import hashlib
import io
import re
from pathlib import Path
from typing import Literal
from urllib.parse import urljoin
from zipfile import ZipFile

from django.http import FileResponse, HttpRequest, HttpResponse
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
def upload(
    request: HttpRequest,
    content: UploadedFile = File(...),
    metadata: Metadata = Form(...),
):
    if not content.name.endswith((".tar.gz", ".whl")):
        msg = "Only '.tar.gz' and '.whl' files are supported."
        raise HttpError(400, msg)

    if Package.objects.filter(filename=content.name).exists():
        msg = f"Package with this name({content.name}) already exists."
        raise HttpError(400, msg)

    package = Package.objects.create(
        name=normalize(metadata.name),
        version=metadata.version,
        file=content,
        filename=content.name,
        sha256=get_sha256(content, metadata),
        metadata=get_metadata(content),
        requires_python=metadata.requires_python,
    )
    return urljoin(request.build_absolute_uri("/"), package.file.url)


@router.get("/")
def index(request: HttpRequest, response: HttpResponse):
    response["Content-Type"] = "application/vnd.pypi.simple.v1+json"
    ret = {"meta": {"api-version": "1.0"}}

    names = Package.objects.values_list("name", flat=True).distinct().order_by("name")
    ret["projects"] = [{"name": name} for name in names]
    return ret


@router.get("/{name}/")
def packages(
    request: HttpRequest,
    response: HttpResponse,
    name: str,
):
    name = normalize(name)

    packages = Package.objects.filter(name=name)
    if not packages.exists():
        msg = f"{name!r} package does not exist."
        raise HttpError(404, msg)

    response["Content-Type"] = "application/vnd.pypi.simple.v1+json"
    ret = {"meta": {"api-version": "1.0"}, "name": name, "files": []}

    for package in packages:
        data = {
            "filename": package.filename,
            "url": urljoin(request.build_absolute_uri("/"), package.file.url),
            "hashes": {"sha256": package.sha256},
        }
        if package.requires_python:
            data["requires-python"] = package.requires_python
        if package.metadata:
            data["dist-info-metadata"] = package.dist_info_metadata
        ret["files"].append(data)
    return ret


@router.get("/{name}/{filename}")
def download(
    request: HttpRequest,
    name: str,
    filename: str,
):
    name = normalize(name)

    metadata = False
    if filename.endswith(".metadata"):
        metadata = True
        filename = filename.removesuffix(".metadata")

    try:
        package = Package.objects.get(filename=filename)
    except Package.DoesNotExist as e:
        msg = f"{name!r} package does not exist."
        raise HttpError(404, msg) from e

    if not Path(package.file.path).exists():
        package.delete()
        msg = f"{name!r} package does not exist."
        raise HttpError(404, msg)

    if metadata:
        return FileResponse(io.BytesIO(package.metadata))
    return FileResponse(package.file)
