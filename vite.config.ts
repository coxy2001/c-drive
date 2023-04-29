import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [svelte()],
    build: {
        outDir: "static/dist/",
        emptyOutDir: true,
        assetsDir: "",
        manifest: true,
        rollupOptions: {
            input: "static/src/main.ts",
        },
    },
});
