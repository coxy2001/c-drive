<script lang="ts">
    import File from "./File.svelte";

    let folders = [];
    let files = [];

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

    fetch("/files/").then(async (response) => {
        const json = await response.json();
        folders = json.folders;
        files = json.files;
    });
</script>

<header class="header">
    <h2>C-Drive</h2>
</header>

<main>
    <div class="grid">
        {#each folders as folder}
            <File file={folder} />
        {/each}
    </div>

    <div class="grid">
        {#each files as file}
            <File {file} />
        {/each}
    </div>
</main>
