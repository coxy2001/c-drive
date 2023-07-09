const getCookieValue = (name: string) =>
    document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)")?.pop() || "";

const CSRF_TOKEN = getCookieValue("csrftoken");
const BASE = import.meta.env.VITE_API_URL;

export function getFiles(src: string | null) {
    const url = new URL("files", BASE);

    if (src) url.searchParams.set("source", src);
    else url.searchParams.delete("source");

    return fetch(url);
}

export function uploadFiles(
    dst: string,
    files: FileList,
    ajax: XMLHttpRequest
) {
    const url = new URL("upload", BASE);

    const upload_data = new FormData();
    upload_data.append("destination", dst);
    for (let i = 0; i < files.length; i++) {
        upload_data.append(`file_${i}`, files[i]);
    }

    ajax.open("POST", url);
    ajax.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
    ajax.send(upload_data);
}

export function deleteFile(src: string) {
    const url = new URL("delete", BASE);
    const request = new Request(url, {
        method: "DELETE",
        headers: { "X-CSRFToken": CSRF_TOKEN },
        body: JSON.stringify({ source: src }),
    });
    return fetch(request);
}

export function moveFile(src: string, dst: string) {
    const url = new URL("move", BASE);
    const request = new Request(url, {
        method: "PUT",
        headers: { "X-CSRFToken": CSRF_TOKEN },
        body: JSON.stringify({ source: src, destination: dst }),
    });
    return fetch(request);
}

export function renameFile(src: string, name: string) {
    const url = new URL("rename", BASE);
    const request = new Request(url, {
        method: "PUT",
        headers: { "X-CSRFToken": CSRF_TOKEN },
        body: JSON.stringify({ source: src, name: name }),
    });
    return fetch(request);
}
