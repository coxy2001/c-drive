<script lang="ts">
    import { fade } from "svelte/transition";
    import { moveFile } from "../api";

    export let file,
        action = (_) => {};

    let folder = file.type == "folder",
        showOptions = false,
        hovering = false,
        optionList: HTMLElement;

    // File actions
    function actionRename() {}
    function actionDelete() {}

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
        e.dataTransfer.setData("path", file.path);
    }

    function drop(e: DragEvent) {
        hovering = false;
        if (e.dataTransfer.getData("path") != file.path) {
            moveFile(e.dataTransfer.getData("path"), file.path);
        }
    }

    function dragOver(e: DragEvent) {
        if (folder) {
            e.preventDefault();
            hovering = true;
        }
    }

    function dragLeave() {
        if (folder) hovering = false;
    }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div
    class="file"
    class:file--selected={file.selected}
    class:file--hovering={hovering}
    draggable="true"
    on:click={() => action(file)}
    on:contextmenu={openOptions}
    on:dragstart={dragStart}
    on:drop={drop}
    on:dragover={dragOver}
    on:dragleave={dragLeave}
>
    {#if !folder}
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
                {#if folder}Open{:else}Preview{/if}
            </button>
            {#if !folder}
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
