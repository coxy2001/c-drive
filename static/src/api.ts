declare global {
    interface Window {
        basePath: string;
        csrftoken: string;
    }
}

const DOMAIN = "http://localhost:8000";

export function getFiles(src: string) {
    let url = new URL("files", DOMAIN);

    if (src) url.searchParams.set("source", src);
    else url.searchParams.delete("source");

    return fetch(url);
}

export function deleteFile(src: string) {
    let url = new URL("delete", DOMAIN);
    const request = new Request(url, {
        method: "DELETE",
        headers: { "X-CSRFToken": window.csrftoken },
        body: JSON.stringify({ source: src }),
    });
    return fetch(request);
}
export function moveFile(src: string, dst: string) {
    let url = new URL("move", DOMAIN);
    const request = new Request(url, {
        method: "PUT",
        headers: { "X-CSRFToken": window.csrftoken },
        body: JSON.stringify({ source: src, destination: dst }),
    });
    return fetch(request);
}

export function renameFile(src: string, name: string) {
    let url = new URL("rename", DOMAIN);
    const request = new Request(url, {
        method: "PUT",
        headers: { "X-CSRFToken": window.csrftoken },
        body: JSON.stringify({ source: src, name: name }),
    });
    return fetch(request);
}
