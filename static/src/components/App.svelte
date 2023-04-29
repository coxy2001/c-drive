<script lang="ts">
    import File from "./File.svelte";

    import { getFiles } from "../api";

    let folders = [],
        files = [],
        breadcrumbs = [],
        previewFile;

    document.body.addEventListener("contextmenu", (e) => {
        e.preventDefault();
    });

    $: {
        let dir = "";
        breadcrumbs.forEach((breadcrumb) => {
            dir += breadcrumb + "/";
        });

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

    function navigate(file: any) {
        breadcrumbs = [...breadcrumbs, file.name];
    }

    function preview(file: any) {
        previewFile = file;
    }

    function revert(index: number) {
        return () => {
            breadcrumbs = breadcrumbs.slice(0, index);
        };
    }
</script>

<header class="header">
    <h2>C-Drive</h2>
</header>

<main>
    <div class="breadcrumbs">
        <button class="breadcrumbs__item" on:click={revert(0)}>Home</button>
        {#each breadcrumbs as breadcrumb, index}
            &raquo;
            <button class="breadcrumbs__item" on:click={revert(index + 1)}>
                {breadcrumb}
            </button>
        {/each}
    </div>

    {#if folders.length > 0}
        <div class="grid">
            {#each folders as folder}
                <File file={folder} action={navigate} />
            {/each}
        </div>
    {/if}

    {#if files.length > 0}
        <div class="grid">
            {#each files as file}
                <File {file} action={preview} />
            {/each}
        </div>
    {/if}
</main>

{#if previewFile}
    <div class="preview">
        <img src={previewFile.thumbnail} alt={previewFile.name} />
    </div>
{/if}
