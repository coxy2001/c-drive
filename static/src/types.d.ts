export interface Item {
    name: string;
    path: string;
    type?: string;
    url?: string;
    thumbnail?: string;
}

export interface FilesResponse {
    breadcrumbs: Item[];
    folders: Item[];
    files: Item[];
}
