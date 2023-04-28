import os
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from c_drive.settings import BASE_PATH


@login_required
def index(request):
    return render(request, "base.html")


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
