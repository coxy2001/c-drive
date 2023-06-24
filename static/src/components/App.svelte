<script lang="ts">
    import Breadcrumb from "./Breadcrumb.svelte";
    import File from "./File.svelte";
    import { getFiles } from "../api";
    import type { FilesResponse, Item } from "../types";
    import PreviewModal from "./PreviewModal.svelte";

    let currentPath: string | null,
        breadcrumbs: Item[] = [],
        folders: Item[] = [],
        files: Item[] = [],
        previewFile: Item | null,
        previewOpen = false;

    window.addEventListener("popstate", (e) => (currentPath = e.state));
    document.body.addEventListener("contextmenu", (e) => e.preventDefault());

    currentPath = new URLSearchParams(window.location.search).get("path");

    $: {
        updateFiles(currentPath);
    }

    function updateFiles(dir: string | null) {
        getFiles(dir).then(async (response) => {
            if (response.ok) {
                const json: FilesResponse = await response.json();
                breadcrumbs = json.breadcrumbs;
                folders = json.folders;
                files = json.files;
            } else {
                console.log(response.status);
            }
        });
    }

    function pushHistory(dir: string | null) {
        if (window.history.state != dir)
            window.history.pushState(
                dir,
                "",
                dir ? `?path=${encodeURIComponent(dir)}` : "/"
            );
    }

    function navigate(file: Item) {
        currentPath = file.path;
        pushHistory(currentPath);
    }

    function preview(file: Item) {
        previewFile = file;
        previewOpen = true;
    }

    function remove(index: number, isFolder: boolean) {
        return () => {
            if (isFolder) {
                folders.splice(index, 1);
                folders = folders;
            } else {
                files.splice(index, 1);
                files = files;
            }
        };
    }
</script>

<header class="header">
    <h2>C-Drive</h2>
</header>

<main>
    <div class="breadcrumbs">
        {#each breadcrumbs as breadcrumb, index}
            {#if index > 0}&raquo;{/if}
            <Breadcrumb
                {breadcrumb}
                action={navigate}
                last={breadcrumbs.length == index + 1}
            />
        {/each}
    </div>

    {#if folders.length > 0}
        <div class="grid" role="grid">
            {#each folders as folder, index}
                <File
                    file={folder}
                    action={navigate}
                    on:remove={remove(index, true)}
                />
            {/each}
        </div>
    {/if}

    {#if files.length > 0}
        <div class="grid" role="grid">
            {#each files as file, index}
                <File
                    {file}
                    action={preview}
                    on:remove={remove(index, false)}
                />
            {/each}
        </div>
    {/if}
</main>

{#if previewFile && previewOpen}
    <PreviewModal file={previewFile} close={() => (previewOpen = false)} />
{/if}
