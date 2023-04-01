<script lang="ts">
    import File from "./File.svelte";

    let folders = [];
    for (let i = 0; i < 6; i++) {
        folders.push({
            name: "Folder",
            type: "folder",
            selected: i % 2,
        });
    }

    let files = [];
    for (let i = 0; i < 20; i++) {
        files.push({
            name: "File name",
            type: "png",
            thumbnail:
                "https://coxy.tech/jw__pillars-of-creation--1920x1080.jpg",
            selected: i % 2,
        });
    }
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
