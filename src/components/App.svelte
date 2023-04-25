<script lang="ts">
    import File from "./File.svelte";

    const DOMAIN = "http://localhost:8000";

    let folders = [],
        files = [],
        breadcrumbs = [],
        filesURL = new URL("/files/", DOMAIN);

    document.body.addEventListener("contextmenu", (e) => {
        e.preventDefault();

        let cmWidth = 100; // contextMenu.offsetWidth
        let cmHeight = 100; // contextMenu.offsetHeight
        let subMenuWidth = 100;
        let subMenuLeft = false;

        let x = e.offsetX;
        if (x > window.innerWidth - cmWidth - subMenuWidth) subMenuLeft = true;
        if (x > window.innerWidth - cmWidth) x = window.innerWidth - cmWidth;

        let y = e.offsetY;
        if (y > window.innerHeight - cmHeight)
            y = window.innerHeight - cmHeight;
    });

    $: {
        if (breadcrumbs.length > 0) {
            let path = "";
            breadcrumbs.forEach((breadcrumb) => {
                path += breadcrumb + "/";
            });
            filesURL.searchParams.set("dir", path);
        } else {
            filesURL.searchParams.delete("dir");
        }

        fetch(filesURL).then(async (response) => {
            const json = await response.json();
            console.log(json);
            folders = json.folders;
            files = json.files;
        });
    }

    function navigate(name: string) {
        breadcrumbs = [...breadcrumbs, name];
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
                <File file={folder} {navigate} />
            {/each}
        </div>
    {/if}

    {#if files.length > 0}
        <div class="grid">
            {#each files as file}
                <File {file} />
            {/each}
        </div>
    {/if}
</main>
