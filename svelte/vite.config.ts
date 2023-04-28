import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [svelte()],
    build: {
        outDir: "../static/svelte/",
        emptyOutDir: true,
        assetsDir: "",
        manifest: true,
        rollupOptions: {
            input: "src/main.ts",
        },
    },
});
