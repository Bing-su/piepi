from __future__ import annotations

import hashlib

from django.db import models


def directory_path(instance: Package, filename: str):
    return f"{instance.name}/{filename}"


class Package(models.Model):
    name = models.CharField(max_length=255, editable=False)
    file = models.FileField(upload_to=directory_path)
    filename = models.CharField(max_length=255, editable=False, unique=True)
    sha256 = models.CharField(max_length=64, editable=False)

    metadata = models.BinaryField(blank=True)
    requires_python = models.CharField(max_length=64, blank=True, editable=False)

    @property
    def dist_info_metadata(self) -> str:
        return hashlib.sha256(self.metadata).hexdigest()

    def __repr__(self):
        return f"<Package {self.filename!r}>"

    def __str__(self):
        return self.filename
