from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

import json

from .settings import BASE_PATH, SVELTE_DEBUG
from pathlib import Path


@login_required
def index(request: HttpRequest):
    svelte_js, svelte_css = svelte_files()

    context = {
        "base_path": BASE_PATH.replace("\\", "\\\\"),
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

    dir = Path(request.GET.get("source", BASE_PATH)).resolve()
    if not dir.exists():
        return JsonResponse({"error": "invalid path"})

    for path in dir.iterdir():
        if path.is_dir():
            folders.append(
                {
                    "name": path.name,
                    "path": str(path / "X")[:-1],
                    "type": "folder",
                }
            )
        else:
            files.append(
                {
                    "name": path.name,
                    "path": str(path),
                    "type": "",
                    "thumbnail": str(path).replace(BASE_PATH, "/"),
                }
            )

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

    return JsonResponse(
        {
            "name": path.name,
            "path": str(path),
            "type": "folder" if path.is_dir() else "",
            "thumbnail": str(path).replace(BASE_PATH, "/"),
        }
    )
