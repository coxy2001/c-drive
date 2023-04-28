from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

import json
import os

from .settings import BASE_PATH, DEBUG


@login_required
def index(request):
    svelte_js = "http://localhost:5173/src/main.ts"
    svelte_css = []
    if not DEBUG:
        with open("static/svelte/manifest.json", "r") as file:
            manifest = json.loads(file.read())
            svelte_js = "/static/svelte/" + manifest["src/main.ts"]["file"]
            for css in manifest["src/main.ts"].get("css", []):
                svelte_css.append("/static/svelte/" + css)

    context = {
        "svelte_js": svelte_js,
        "svelte_css": svelte_css,
    }
    return render(request, "base.html", context)


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
