import { mdsvex } from "mdsvex";
import remarkGfm from "remark-gfm";
import rehypeExternalLinks from "rehype-external-links"

import adapter from "@sveltejs/adapter-static";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  extensions: [".svelte", ".md", ".svx"],
  preprocess: [
    mdsvex({
      extensions: [".md", ".svx"],
      remarkPlugins: [remarkGfm],
      rehypePlugins: [rehypeExternalLinks],
      smartypants: true,
    }),
    vitePreprocess(),
  ],
  kit: {
    adapter: adapter({
      pages: "build",
      assets: "build",
      fallback: undefined,
      precompress: true,
      strict: true,
    }),
    alias: {
      $lib: "./src/lib",
    },
  },
};

export default config;
