from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse

import json

from c_drive.settings import BASE_PATH
from pathlib import Path
from urllib.parse import quote


@login_required
def files(request: HttpRequest):
    files, folders = [], []

    base = request.user.profile.path()
    dir = base
    if "source" in request.GET:
        dir /= request.GET["source"]

    if not dir.exists():
        return JsonResponse({"error": "invalid path"})

    for path in dir.iterdir():
        if path.is_dir():
            folders.append(_path_json(path, base))
        else:
            files.append(_path_json(path, base))

    return JsonResponse(
        {
            "folders": folders,
            "files": files,
        }
    )


@login_required
def delete(request: HttpRequest):
    data = json.loads(request.body)
    base = request.user.profile.path()
    # Path(base / data["source"]).unlink()
    return JsonResponse({})


@login_required
def move(request: HttpRequest):
    data = json.loads(request.body)
    base = request.user.profile.path()
    Path(base / data["source"]).rename(base / data["destination"])
    return JsonResponse({})


@login_required
def rename(request: HttpRequest):
    data = json.loads(request.body)
    base = request.user.profile.path()
    path = Path(base / data["source"])
    path = path.rename(path.with_name(data["name"]))
    return JsonResponse(_path_json(path, base))


def _path_json(path: Path, base: Path) -> dict[str, str]:
    data = {
        "name": path.name,
    }
    if path.is_dir():
        data["path"] = str(path.relative_to(base) / "X")[:-1]
        data["type"] = "folder"
    else:
        data["path"] = str(path.relative_to(base))
        data["type"] = ""
        data["url"] = "/static/" + quote(str(path.relative_to(BASE_PATH)))
        if path.stat().st_size < 3 * 1024 * 1024:
            data["thumbnail"] = "/static/" + quote(str(path.relative_to(BASE_PATH)))

    return data
