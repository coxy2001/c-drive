<script lang="ts">
    import { fade } from "svelte/transition";

    export let file;

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

    function deleteFile() {}
</script>

<div class="file" class:file--selected={file.selected}>
    {#if file.type != "folder"}
        <div
            class="file__thumbnail"
            style="background-image: url({file.thumbnail});"
        />
    {/if}
    <div class="file__title">{file.name}</div>
    <button class="file__option-button" on:click={openOptions} />
    {#if options}
        <div
            class="file__option-list"
            tabindex="-1"
            transition:fade={{ duration: 100 }}
            bind:this={optionList}
            on:focusin={() => (options = true)}
            on:focusout={closeOptions}
            on:keydown={(e) => {
                if (e.key == "Escape") options = false;
            }}
        >
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
            <button
                class="file__option"
                on:click={deleteFile}
                on:keydown={deleteFile}
            >
                Delete
            </button>
        </div>
    {/if}
</div>
