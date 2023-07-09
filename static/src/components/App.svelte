<script lang="ts">
    import { fade } from "svelte/transition";
    import Breadcrumb from "./Breadcrumb.svelte";
    import File from "./File.svelte";
    import PreviewModal from "./PreviewModal.svelte";
    import { getFiles, uploadFiles } from "../api";
    import type { FilesResponse, Item } from "../types";

    let currentPath: string | null,
        breadcrumbs: Item[] = [],
        folders: Item[] = [],
        files: Item[] = [],
        hovering = false,
        previewFile: Item | null,
        previewOpen = false,
        upload = false,
        progress: HTMLProgressElement;

    window.addEventListener("popstate", (e) => (currentPath = e.state));
    document.body.addEventListener("contextmenu", (e) => e.preventDefault());

    currentPath = new URLSearchParams(window.location.search).get("path");

    $: updateFiles(currentPath);

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

    function drop(e: DragEvent) {
        e.preventDefault();
        hovering = false;
        if (e.dataTransfer.types.includes("Files")) {
            const ajax = new XMLHttpRequest();
            ajax.upload.addEventListener("progress", (event) => {
                let percent = Math.round((event.loaded / event.total) * 100);
                progress.value = percent;
            });
            ajax.addEventListener("load", (event) => {
                updateFiles(currentPath);
                setTimeout(() => (upload = false), 1000);
            });
            ajax.addEventListener("error", (event) => {
                alert("Upload failed");
            });
            ajax.addEventListener("abort", (event) => {
                alert("Upload aborted");
            });

            upload = true;
            uploadFiles(currentPath || "", e.dataTransfer.files, ajax);
        }
    }

    function dragOver(e: DragEvent) {
        if (e.dataTransfer.types.includes("Files")) {
            e.preventDefault();
            hovering = true;
        }
    }

    function dragLeave(e: DragEvent) {
        hovering = false;
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
        <div
            class="dropzone"
            class:dropzone--hovering={hovering}
            role="button"
            tabindex="-1"
            on:drop={drop}
            on:dragover={dragOver}
            on:dragleave={dragLeave}
        >
            <div class="grid" role="grid">
                {#each files as file, index}
                    <File
                        {file}
                        action={preview}
                        on:remove={remove(index, false)}
                    />
                {/each}
            </div>
        </div>
    {/if}
</main>

{#if upload}
    <div class="upload" transition:fade={{ duration: 200 }}>
        <div class="upload__container">
            <progress
                class="upload__progress"
                value="0"
                max="100"
                bind:this={progress}
            />
        </div>
    </div>
{/if}

{#if previewFile && previewOpen}
    <PreviewModal file={previewFile} close={() => (previewOpen = false)} />
{/if}
