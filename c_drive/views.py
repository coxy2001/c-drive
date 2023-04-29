from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

import json
import os

from .settings import BASE_PATH, SVELTE_DEBUG


@login_required
def index(request):
    svelte_js, svelte_css = svelte_files()

    context = {
        "svelte_js": svelte_js,
        "svelte_css": svelte_css,
    }
    return render(request, "base.html", context)


def svelte_files():
    SVELTE_DIST = "static/dist/"
    svelte_js = "http://localhost:5173/static/src/main.ts"
    svelte_css = []

    if not SVELTE_DEBUG:
        with open(SVELTE_DIST + "manifest.json", "r") as file:
            main_manifest = json.loads(file.read())["src/main.ts"]
            svelte_js = "/" + SVELTE_DIST + main_manifest["file"]
            for css in main_manifest.get("css", []):
                svelte_css.append("/" + SVELTE_DIST + css)

    return svelte_js, svelte_css


@login_required
def files(request):
    files, folders = [], []

    path = BASE_PATH + request.GET.get("dir", "")
    if not os.path.exists(path):
        return JsonResponse({"error": "invalid path"})

    for item in os.scandir(path):
        if item.is_dir():
            folders.append(
                {
                    "name": item.name,
                    "type": "folder",
                }
            )
        else:
            files.append(
                {
                    "name": item.name,
                    "type": "",
                    "thumbnail": item.path.replace(BASE_PATH, "/"),
                }
            )

    return JsonResponse(
        {
            "folders": folders,
            "files": files,
        }
    )
