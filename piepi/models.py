from __future__ import annotations

import hashlib

from django.db import models


def directory_path(instance: Package, filename: str):
    return f"{instance.name}/{filename}"


class Package(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=directory_path)
    filename = models.CharField(max_length=255, unique=True)
    sha256 = models.CharField(max_length=64)

    metadata = models.BinaryField(blank=True)
    requires_python = models.CharField(max_length=64, blank=True)

    @property
    def dist_info_metadata(self) -> str:
        return hashlib.sha256(self.metadata).hexdigest()
