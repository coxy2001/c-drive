<script lang="ts">
    import { moveFile } from "../api";
    import type { Item } from "../types";

    export let breadcrumb: Item, action: (_: Item) => void, last: boolean;

    let hovering = false;

    function drop(e: DragEvent) {
        hovering = false;
        const name = e.dataTransfer.getData("name");
        const path = e.dataTransfer.getData("path");
        if (name && path) {
            moveFile(path, breadcrumb.path + name);
        }
    }

    function dragOver(e: DragEvent) {
        if (!last) {
            e.preventDefault();
            hovering = true;
        }
    }

    function dragLeave() {
        hovering = false;
    }
</script>

<button
    class="breadcrumbs__item"
    class:breadcrumbs__item--hovering={hovering}
    on:click={() => action(breadcrumb)}
    on:drop={drop}
    on:dragover={dragOver}
    on:dragleave={dragLeave}
>
    {breadcrumb.name}
</button>
