from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

import json

from .settings import SVELTE_DEBUG


@login_required
def index(request: HttpRequest):
    svelte_js, svelte_css = _svelte_files()

    context = {
        "svelte_js": svelte_js,
        "svelte_css": svelte_css,
    }
    return render(request, "base.html", context)


def _svelte_files() -> tuple[str, list[str]]:
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
