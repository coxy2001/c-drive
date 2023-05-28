from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

import json

from .settings import BASE_PATH, SVELTE_DEBUG
from pathlib import Path
from urllib.parse import quote


@login_required
def index(request: HttpRequest):
    svelte_js, svelte_css = svelte_files()

    context = {
        "base_path": str(BASE_PATH).replace("\\", "\\\\"),
        "svelte_js": svelte_js,
        "svelte_css": svelte_css,
    }
    return render(request, "base.html", context)


def svelte_files() -> tuple[str, list[str]]:
    SVELTE_DIST = "static/dist/"
    svelte_js = "http://localhost:5173/static/src/main.ts"
    svelte_css = []

    if not SVELTE_DEBUG:
        with open(SVELTE_DIST + "manifest.json", "r") as file:
            main_manifest = json.loads(file.read())["static/src/main.ts"]
            svelte_js = "/" + SVELTE_DIST + main_manifest["file"]
            for css in main_manifest.get("css", []):
                svelte_css.append("/" + SVELTE_DIST + css)

    return svelte_js, svelte_css


@login_required
def files(request: HttpRequest):
    files, folders = [], []

    dir = BASE_PATH
    if "source" in request.GET:
        dir /= request.GET["source"]

    if not dir.exists():
        return JsonResponse({"error": "invalid path"})

    for path in dir.iterdir():
        if path.is_dir():
            folders.append(path_json(path))
        else:
            files.append(path_json(path))

    return JsonResponse(
        {
            "folders": folders,
            "files": files,
        }
    )


@login_required
def delete(request: HttpRequest):
    data = json.loads(request.body)
    # Path(data["source"]).unlink()
    return JsonResponse({})


@login_required
def move(request: HttpRequest):
    data = json.loads(request.body)
    print(data)
    Path(data["source"]).rename(data["destination"])
    return JsonResponse({})


@login_required
def rename(request: HttpRequest):
    data = json.loads(request.body)
    path = Path(data["source"])
    path = path.rename(path.with_name(data["name"]))

    return JsonResponse(path_json(path))


def path_json(path: Path) -> dict[str, str]:
    data = {
        "name": path.name,
    }
    if path.is_dir():
        data["path"] = str(path.relative_to(BASE_PATH) / "X")[:-1]
        data["type"] = "folder"
    else:
        data["path"] = str(path.relative_to(BASE_PATH))
        data["type"] = ""
        data["url"] = "/static/" + quote(str(path.relative_to(BASE_PATH)))
        if path.stat().st_size < 3 * 1024 * 1024:
            data["thumbnail"] = "/static/" + quote(str(path.relative_to(BASE_PATH)))

    return data
