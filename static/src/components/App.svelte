<script lang="ts">
    import Breadcrumb from "./Breadcrumb.svelte";
    import File from "./File.svelte";
    import { getFiles } from "../api";
    import type { Item } from "../types";
    import PreviewModal from "./PreviewModal.svelte";

    let folders: Item[] = [],
        files: Item[] = [],
        breadcrumbs: Item[] = [{ name: "Home", path: window.basePath }],
        previewFile: Item | null,
        previewOpen = false;

    document.body.addEventListener("contextmenu", (e) => e.preventDefault());

    $: {
        let dir = breadcrumbs[breadcrumbs.length - 1].path;
        updateFiles(dir);
    }

    function updateFiles(dir: string) {
        getFiles(dir).then(async (response) => {
            if (response.ok) {
                const json = await response.json();
                folders = json.folders;
                files = json.files;
            } else {
                console.log(response.status);
            }
        });
    }

    function navigate(file: Item) {
        breadcrumbs = [...breadcrumbs, file];
    }

    function preview(file: Item) {
        previewFile = file;
        previewOpen = true;
    }

    function revert(index: number) {
        return () => (breadcrumbs = breadcrumbs.slice(0, index + 1));
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
                revert={revert(index)}
                last={breadcrumbs.length == index + 1}
            />
        {/each}
    </div>

    {#if folders.length > 0}
        <div class="grid">
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
        <div class="grid">
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
