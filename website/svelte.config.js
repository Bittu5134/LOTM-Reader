import adapter from "@sveltejs/adapter-static";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  extensions: [".svelte"],
  preprocess: [
    vitePreprocess(),
  ],
  kit: {
    adapter: adapter({
      pages: "build",
      assets: "build",
      fallback: "404.html",
      precompress: true,
      strict: true,
    }),

    prerender: {
      concurrency: 5,
      crawl: true,
      handleHttpError: "warn",
    },

    alias: {
      $lib: "./src/lib",
    },
  },
};

export default config;
