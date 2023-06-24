const getCookieValue = (name: string) =>
    document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)")?.pop() || "";

const CSRF_TOKEN = getCookieValue("csrftoken");
const BASE = "http://localhost:8000/api/";

export function getFiles(src: string | null) {
    let url = new URL("files", BASE);

    if (src) url.searchParams.set("source", src);
    else url.searchParams.delete("source");

    return fetch(url);
}

export function deleteFile(src: string) {
    let url = new URL("delete", BASE);
    const request = new Request(url, {
        method: "DELETE",
        headers: { "X-CSRFToken": CSRF_TOKEN },
        body: JSON.stringify({ source: src }),
    });
    return fetch(request);
}

export function moveFile(src: string, dst: string) {
    let url = new URL("move", BASE);
    const request = new Request(url, {
        method: "PUT",
        headers: { "X-CSRFToken": CSRF_TOKEN },
        body: JSON.stringify({ source: src, destination: dst }),
    });
    return fetch(request);
}

export function renameFile(src: string, name: string) {
    let url = new URL("rename", BASE);
    const request = new Request(url, {
        method: "PUT",
        headers: { "X-CSRFToken": CSRF_TOKEN },
        body: JSON.stringify({ source: src, name: name }),
    });
    return fetch(request);
}
