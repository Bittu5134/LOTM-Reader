<script lang="ts">
  import Icon from "@iconify/svelte";
  import { onMount } from "svelte";
  import { render } from "svelte/server";
  import { page } from "$app/state";

  // State
  let activeId = $state("");
  let rulesModal: HTMLDialogElement;

  const BANNERS = [
    { id: "discord", weight: 1 },
    { id: "github", weight: 1 },
    { id: "donate", weight: 2 },
    { id: "keybinds", weight: 1 },
    { id: "formatting", weight: 1 },
    { id: "download", weight: 1 },
    { id: "none", weight: 0 },
  ];

  function getWeightedBanner() {
    const totalWeight = BANNERS.reduce((sum, item) => sum + item.weight, 0);
    let random = Math.random() * totalWeight;

    for (const banner of BANNERS) {
      if (random < banner.weight) return banner.id;
      random -= banner.weight;
    }
    return BANNERS[0].id;
  }

$effect(() => {
    const _ = page.url.href; 
    activeId = getWeightedBanner();
  });
</script>

{#if activeId}
  <div
    class="flex justify-center pb-8 px-4 opacity-75 hover:opacity-100 transition-all duration-300"
  >
    <div
      class="w-full max-w-3xl rounded-box border border-amber-50/10 bg-base-200 p-5"
    >
      {#if activeId === "discord"}
        {@render discordBanner()}
      {:else if activeId === "github"}
        {@render githubBanner()}
      {:else if activeId === "donate"}
        {@render donateBanner()}
      {:else if activeId === "keybinds"}
        {@render keybindsBanner()}
      {:else if activeId === "formatting"}
        {@render formattingBanner()}
      {:else if activeId === "download"}
        {@render downloadBanner()}
      {:else if activeId === "none"}
        <br />
      {/if}
    </div>
  </div>
{/if}

{#snippet discordBanner()}
  <div
    class="flex flex-col md:flex-row items-center justify-between gap-4 md:gap-6"
  >
    <div class="text-center md:text-left">
      <p
        class="text-base font-bold flex items-center justify-center md:justify-start gap-2"
      >
        <Icon icon="ic:baseline-discord" class="text-[#5865F2] size-5" />
        Join the Community
      </p>
      <p class="text-sm opacity-70 mt-1">
        Discuss theories, report TL errors, recommend Illustrations or just chat
        with other readers.
      </p>
    </div>
    <a
      href="https://discord.gg/XmzJVsyuTQ"
      target="_blank"
      rel="noopener noreferrer"
      class="btn btn-sm bg-[#5865F2] hover:bg-[#4752C4] text-white border-0 min-w-30"
    >
      Join Server
    </a>
  </div>
{/snippet}

{#snippet githubBanner()}
  <div
    class="flex flex-col md:flex-row items-center justify-between gap-4 md:gap-6"
  >
    <div class="text-center md:text-left">
      <p
        class="text-base font-bold flex items-center justify-center md:justify-start gap-2"
      >
        <Icon icon="mdi:github" class="size-5" />
        Open Source
      </p>
      <p class="text-sm opacity-70 mt-1">
        Intrested in the code? Want to add a feature? Check out the repo!
      </p>
    </div>
    <div class="flex gap-2">
      <a
        href="https://github.com/Bittu5134/LOTM-Reader"
        target="_blank"
        class="btn btn-sm btn-neutral"
      >
        <Icon icon="mdi:star-outline" class="size-4" /> Star
      </a>
      <a
        href="https://github.com/Bittu5134/"
        target="_blank"
        class="btn btn-sm btn-outline"
      >
        Developer
      </a>
    </div>
  </div>
{/snippet}

{#snippet donateBanner()}
  <div
    class="flex flex-col md:flex-row items-center justify-between gap-4 md:gap-6"
  >
    <div class="text-center md:text-left">
      <p
        class="text-base font-bold flex items-center justify-center md:justify-start gap-2"
      >
        <Icon icon="mdi:heart" class="text-orange-500 size-5" />
        Support the Dev
      </p>
      <p class="text-xs opacity-60 mt-1">
        Enjoying the reader? Consider buying a coffee to keep the servers
        running.
      </p>
    </div>
    <a
      href="/donate"
      target="_blank"
      class="btn btn-sm bg-orange-500 hover:bg-orange-600 text-white border-0 min-w-30"
    >
      <Icon icon="mdi:coffee" class="size-4" /> Donate
    </a>
  </div>
{/snippet}

{#snippet keybindsBanner()}
  <div class="flex flex-col items-center gap-3 py-1">
    <p class="text-sm font-bold uppercase tracking-widest opacity-40">
      Keyboard Shortcuts
    </p>
    <div class="flex flex-wrap justify-center gap-3 text-xs font-mono">
      <div class="flex items-center gap-1">
        <kbd class="kbd kbd-xs">N</kbd> Next
      </div>
      <div class="flex items-center gap-1">
        <kbd class="kbd kbd-xs">P</kbd> Prev
      </div>
      <div class="flex items-center gap-1">
        <kbd class="kbd kbd-xs">F</kbd> Fullscreen
      </div>
      <div class="flex items-center gap-1">
        <kbd class="kbd kbd-xs">T</kbd> Chapter List
      </div>
      <div class="flex items-center gap-1">
        <kbd class="kbd kbd-xs">S</kbd> Settings
      </div>
      <div class="flex items-center gap-1">
        <kbd class="kbd kbd-xs">C</kbd> Comments
      </div>
    </div>
  </div>
{/snippet}

{#snippet formattingBanner()}
  <div
    class="flex flex-col md:flex-row items-center justify-between gap-4 md:gap-6"
  >
    <div class="text-center md:text-left">
      <p
        class="text-base font-bold flex items-center justify-center md:justify-start gap-2"
      >
        <Icon icon="mdi:markdown" class="opacity-70 size-5" />
        Comment Guidelines
      </p>
      <p class="text-xs opacity-60 mt-1">
        Supports Markdown: <span class="font-bold">**bold**</span>,
        <span class="italic">*italics*</span>, and <code>`code`</code>.
      </p>
    </div>
    <button
      onclick={() => rulesModal?.showModal()}
      class="btn btn-sm btn-outline min-w-[120px]"
    >
      Read Rules
    </button>
  </div>
{/snippet}

{#snippet downloadBanner()}
  <div
    class="flex flex-col md:flex-row items-center justify-between gap-4 md:gap-6"
  >
    <div class="text-center md:text-left">
      <p
        class="text-base font-bold flex items-center justify-center md:justify-start gap-2"
      >
        <Icon icon="mdi:cloud-download" class="text-success size-5" />
        Read Offline
      </p>
      <p class="text-xs opacity-60 mt-1">
        Download this book as an EPUB to read on your e-reader or tablet.
      </p>
    </div>
    <a href="/download" class="btn btn-sm btn-success border-0 min-w-30">
      <Icon icon="mdi:download" class="size-4" /> Download
    </a>
  </div>
{/snippet}

<dialog bind:this={rulesModal} class="modal modal-bottom sm:modal-middle">
  <div class="modal-box bg-base-100 max-w-lg">
    <form method="dialog">
      <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
        >✕</button
      >
    </form>

    <h3 class="font-bold text-lg mb-4 flex items-center gap-2">
      <Icon icon="mdi:book-open-page-variant" class="text-primary" />
      Chat Rules & Formatting
    </h3>

    <div class="alert alert-warning mb-6 p-3 rounded-lg">
      <Icon icon="mdi:alert-octagon" class="size-6" />
      <div class="text-sm">
        <h4 class="font-bold">No Spoilers Allowed!</h4>
        <p class="text-xs opacity-80">
          Please keep chapter discussions spoiler-free.
        </p>
        <div class="mt-2 flex gap-2">
          <a
            href="https://discord.gg/lordofthemysteries"
            target="_blank"
            class="link link-hover text-xs font-bold flex items-center gap-1"
          >
            <Icon icon="ic:baseline-discord" /> Discuss on Discord
          </a>
          <a
            href="https://reddit.com/r/LordOfTheMysteries"
            target="_blank"
            class="link link-hover text-xs font-bold flex items-center gap-1"
          >
            <Icon icon="mdi:reddit" /> Visit Subreddit
          </a>
        </div>
      </div>
    </div>

    <div class="space-y-4">
      <h4
        class="text-sm font-bold uppercase tracking-widest opacity-50 border-b border-base-content/10 pb-1"
      >
        Markdown Guide
      </h4>

      <div class="overflow-x-auto">
        <table class="table table-xs w-full">
          <thead>
            <tr>
              <th>Style</th>
              <th>Syntax</th>
              <th>Output</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Bold</td>
              <td class="font-mono text-xs">**text**</td>
              <td class="font-bold">text</td>
            </tr>
            <tr>
              <td>Italics</td>
              <td class="font-mono text-xs">*text*</td>
              <td class="italic">text</td>
            </tr>
            <tr>
              <td>Code</td>
              <td class="font-mono text-xs">`text`</td>
              <td><code class="bg-base-300 rounded px-1">text</code></td>
            </tr>
            <tr>
              <td>Quote</td>
              <td class="font-mono text-xs">> text</td>
              <td class="prose text-xs"><blockquote>test</blockquote></td>
            </tr>
            <tr>
              <td>Image</td>
              <td class="font-mono text-xs">![](url)</td>
              <td><Icon icon="mdi:image" class="opacity-50" /></td>
            </tr>
          </tbody>
        </table>
        <a
          class="btn btn-link w-full justify-center"
          href="https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#styling-text"
          >View Guide On Github</a
        >
      </div>

      <div class="bg-base-200/50 p-3 rounded-lg text-sm">
        <p class="font-bold mb-1 flex items-center gap-1">
          <Icon icon="mdi:eye-off" /> How to hide spoilers:
        </p>
        <p class="text-xs opacity-70 mb-2">
          Use HTML tags to create a collapsible section.
        </p>
        <div class="mockup-code bg-base-300 text-base-content p-2 min-w-0">
          <pre class="text-xs"><code
              >&lt;details&gt;
  &lt;summary&gt;Spoiler Warning&lt;/summary&gt;
  The truth about the Fool is...
  &lt;/details&gt;</code
            ></pre>
        </div>
        <p class="text-xs mt-2 opacity-50">Output:</p>
        <details
          class="cursor-pointer border border-base-content/10 rounded px-2 py-1 mt-1 bg-base-100"
        >
          <summary class="text-xs font-bold text-error">Spoiler Warning</summary
          >
          <span class="text-xs">The truth about the Fool is...</span>
        </details>
      </div>
    </div>
  </div>
  <form method="dialog" class="modal-backdrop"><button>close</button></form>
</dialog>
