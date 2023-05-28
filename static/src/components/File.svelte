<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { fade } from "svelte/transition";
    import { deleteFile, moveFile, renameFile } from "../api";
    import type { Item } from "../types";

    export let file: Item, action: (_: Item) => void;

    const dispatch = createEventDispatcher();

    let isFolder = file.type == "folder",
        showOptions = false,
        selected = false,
        dragging = false,
        hovering = false,
        optionList: HTMLElement;

    // File actions
    function actionRename() {
        const newName = prompt(
            `Rename ${isFolder ? "folder" : "file"}`,
            file.name
        );
        if (!newName) return;

        renameFile(file.path, newName).then(async (response) => {
            if (response.ok) file = await response.json();
        });
    }

    function actionDelete() {
        if (!confirm(`Delete ${isFolder ? "folder" : "file"}`)) return;

        deleteFile(file.path).then(async (response) => {
            if (response.ok) dispatch("remove");
        });
    }

    // Options
    async function openOptions() {
        showOptions = true;
        await optionList;
        optionList.focus();
    }

    function closeOptions() {
        showOptions = false;
    }

    // Drag and drop
    function dragStart(e: DragEvent) {
        dragging = true;
        e.dataTransfer.setData("name", file.name);
        e.dataTransfer.setData("path", file.path);
    }

    function dragEnd(e: DragEvent) {
        dragging = false;
        if (e.dataTransfer.dropEffect !== "none") dispatch("remove");
    }

    function drop(e: DragEvent) {
        hovering = false;
        const name = e.dataTransfer.getData("name");
        const path = e.dataTransfer.getData("path");
        if (path != file.path) {
            moveFile(path, file.path + name);
        }
    }

    function dragOver(e: DragEvent) {
        if (isFolder && !dragging) {
            e.preventDefault();
            hovering = true;
        }
    }

    function dragLeave() {
        if (isFolder) hovering = false;
    }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div
    class="file"
    class:file--selected={selected}
    class:file--dragging={dragging}
    class:file--hovering={hovering}
    draggable="true"
    on:click={() => action(file)}
    on:contextmenu={openOptions}
    on:dragstart={dragStart}
    on:dragend={dragEnd}
    on:drop={drop}
    on:dragover={dragOver}
    on:dragleave={dragLeave}
>
    {#if !isFolder}
        <div
            class="file__thumbnail"
            style="background-image: url({file.thumbnail});"
        />
    {/if}
    <div class="file__title">{file.name}</div>
    <button
        class="file__option-button"
        on:click|stopPropagation={openOptions}
    />

    {#if showOptions}
        <div
            class="file__option-list"
            tabindex="-1"
            transition:fade={{ duration: 100 }}
            bind:this={optionList}
            on:focusin={() => (showOptions = true)}
            on:focusout={closeOptions}
            on:click|stopPropagation
            on:keydown={(e) => {
                if (e.key == "Escape") closeOptions();
            }}
        >
            <button class="file__option" on:click={() => action(file)}>
                {#if isFolder}Open{:else}Preview{/if}
            </button>
            {#if !isFolder}
                <a
                    class="file__option"
                    href={file.thumbnail}
                    target="_blank"
                    download
                >
                    Download
                </a>
            {/if}
            <button class="file__option" on:click={actionRename}>Rename</button>
            <button class="file__option" on:click={actionDelete}>Delete</button>
        </div>
    {/if}
</div>
