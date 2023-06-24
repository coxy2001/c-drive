<script lang="ts">
    import { onDestroy } from "svelte";
    import { fade } from "svelte/transition";

    export let title: string, close: VoidFunction;

    let dialogFly = true;

    const documentWidth = document.documentElement.clientWidth;
    const scrollbarWidth = Math.abs(window.innerWidth - documentWidth);
    if (scrollbarWidth > 0) {
        document.body.style.paddingRight = `${scrollbarWidth}px`;
    }
    document.body.style.overflowY = "hidden";

    onDestroy(() => {
        document.body.style.paddingRight = null;
        document.body.style.overflowY = null;
    });
</script>

<div
    class="modal"
    role="presentation"
    on:click={close}
    on:keypress={close}
    transition:fade={{ duration: 200 }}
    on:introstart={() => {
        dialogFly = false;
    }}
    on:outrostart={() => {
        dialogFly = true;
    }}
>
    <div
        class="modal__dialog"
        class:modal__dialog--fly={dialogFly}
        role="presentation"
        on:click|stopPropagation
        on:keypress|stopPropagation
    >
        <div class="modal__header">
            <div class="modal__header-title">{title}</div>
            <button class="modal__header-close" on:click={close} />
        </div>
        <div class="modal__body">
            <slot>This modal is missing a body</slot>
        </div>
        <div class="modal__footer">
            <slot name="footer">
                <button class="btn btn-secondary" on:click={close}>
                    Close
                </button>
            </slot>
        </div>
    </div>
</div>
