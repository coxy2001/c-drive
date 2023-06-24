<script lang="ts">
    import { onDestroy } from "svelte";
    import { fade } from "svelte/transition";
    import type { Item } from "../types";

    export let file: Item, close: VoidFunction;

    let dialogFly = true,
        modal: HTMLElement;

    const documentWidth = document.documentElement.clientWidth;
    const scrollbarWidth = Math.abs(window.innerWidth - documentWidth);
    if (scrollbarWidth > 0) {
        document.body.style.marginRight = `${scrollbarWidth}px`;
    }
    document.body.style.overflowY = "hidden";

    onDestroy(() => {
        document.body.style.marginRight = null;
        document.body.style.overflowY = null;
    });
</script>

<div
    class="preview-modal"
    tabindex="-1"
    role="presentation"
    bind:this={modal}
    on:click={close}
    on:keydown={(e) => {
        if (e.key == "Escape") close();
    }}
    on:contextmenu|stopPropagation
    transition:fade={{ duration: 200 }}
    on:introstart={() => {
        dialogFly = false;
        modal.focus();
    }}
    on:outrostart={() => {
        dialogFly = true;
    }}
>
    <div
        class="preview-modal__dialog"
        class:preview-modal__dialog--fly={dialogFly}
        role="presentation"
        on:click|stopPropagation
        on:keypress|stopPropagation
    >
        <img class="preview-modal__img" src={file.url} alt={file.name} />
        <button class="preview-modal__close" on:click={close} />
    </div>
</div>
