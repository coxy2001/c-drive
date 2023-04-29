<script lang="ts">
    import { fade } from "svelte/transition";

    export let file,
        action = (_) => {};

    let options = false,
        optionList: HTMLElement;

    async function openOptions() {
        options = true;
        await optionList;
        optionList.focus();
    }

    function closeOptions() {
        options = false;
    }

    function renameFile() {}
    function deleteFile() {}
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div
    class="file"
    class:file--selected={file.selected}
    on:click={() => action(file)}
    on:contextmenu={openOptions}
>
    {#if file.type != "folder"}
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
    {#if options}
        <div
            class="file__option-list"
            tabindex="-1"
            transition:fade={{ duration: 100 }}
            bind:this={optionList}
            on:focusin={() => (options = true)}
            on:focusout={closeOptions}
            on:click|stopPropagation
            on:keydown={(e) => {
                if (e.key == "Escape") closeOptions();
            }}
        >
            <button class="file__option" on:click={() => action(file)}>
                {#if file.type == "folder"}Open{:else}Preview{/if}
            </button>
            {#if file.type != "folder"}
                <a
                    class="file__option"
                    href={file.thumbnail}
                    target="_blank"
                    download
                >
                    Download
                </a>
            {/if}
            <button class="file__option" on:click={renameFile}>Rename</button>
            <button class="file__option" on:click={deleteFile}>Delete</button>
        </div>
    {/if}
</div>
