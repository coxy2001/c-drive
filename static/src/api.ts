const DOMAIN = "http://localhost:8000";

export function getFiles(dir: string) {
    let url = new URL("files/", DOMAIN);

    if (dir) url.searchParams.set("dir", dir);
    else url.searchParams.delete("dir");

    return fetch(url);
}

export function moveFile(src: string, dst: string) {
    let url = new URL("move/", DOMAIN);
    const request = new Request(url, {
        method: "PUT",
        body: `{"source": ${src}, "destination": ${dst}}`,
    });
    return fetch(request);
}

export function renameFile(src: string, name: string) {
    let url = new URL("rename/", DOMAIN);
    const request = new Request(url, {
        method: "PUT",
        body: `{"source": ${src}, "name": ${name}}`,
    });
    return fetch(request);
}
