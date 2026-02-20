<script lang="ts">
  import Icon from "@iconify/svelte";
  import { readerState } from "$lib/reader.svelte.ts";

  let { prefs, bookSlug, bookData, navState = $bindable() } = $props();

  // State
  let modals = $state({
    chapter: null as HTMLDialogElement | null,
    settings: null as HTMLDialogElement | null,
    edit: null as HTMLDialogElement | null,
  });

  // --- Constants: Themes ---
  const PRIORITY_THEMES = [
    "sunset",
    "light",
    "retro",
    "night",
    "business",
    "cupcake",
    "black",
  ];
  const ALL_THEMES = [
    "sunset",
    "light",
    "dark",
    "cupcake",
    "bumblebee",
    "emerald",
    "corporate",
    "synthwave",
    "retro",
    "cyberpunk",
    "valentine",
    "halloween",
    "garden",
    "forest",
    "aqua",
    "lofi",
    "pastel",
    "fantasy",
    "wireframe",
    "black",
    "luxury",
    "dracula",
    "cmyk",
    "autumn",
    "business",
    "acid",
    "lemonade",
    "night",
    "coffee",
    "winter",
    "dim",
    "nord",
  ];
  const MISC_THEMES = ALL_THEMES.filter(
    (t) => !PRIORITY_THEMES.includes(t),
  );

  // --- Constants: Fonts ---
  const BOOK_FONTS = [
    "Alegreya",
    "Bookerly",
    "Roboto",
    "monospace",
    "Merriweather",
  ];

  const SYSTEM_FONTS = [
    "EB Garamond",
    "Crimson Pro",
    "Georgia",
    "Verdana",
    "Arial",
    "sans-serif",
    "Times New Roman",
    "serif",
    "Helvetica",
    "Tahoma",
    "system-ui",
    "Trebuchet MS",
    "Courier New",
  ];

  // Logic
  const chapterList = $derived.by(() => {
    const chapters = bookData[bookSlug]?.[navState.selectedTL] || [];
    const q = navState.searchQuery.toLowerCase();
    return chapters.filter(
      (ch: any) =>
        ch.title.toLowerCase().includes(q) || ch.slug.toString().includes(q),
    );
  });

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      modals.chapter?.close()
      modals.settings?.close()
      modals.edit?.close()
      document.documentElement.requestFullscreen().catch(console.error);
    } else {
      document.exitFullscreen();
    }
  }

  // Exports
  export const openTOC = () => {
    modals.chapter?.showModal();
    setTimeout(() => {
      modals.chapter
        ?.querySelector(".btn-primary")
        ?.scrollIntoView({ block: "center" });
    }, 0);
  };
  export const openSettings = () => modals.settings?.showModal();
  export const openEdit = () => modals.edit?.showModal();
</script>

{#if prefs.config.navbarVisible}
  <nav
    class="flex w-full items-center justify-center gap-5 bg-base-100 border-b border-base-content/10 p-3 z-50 {prefs
      .config.navbarSticky
      ? 'sticky top-0'
      : 'relative'}"
  >
    <div class="tooltip tooltip-bottom" data-tip="Home (H)">
      <a
        href="/book/{bookSlug}"
        class="btn btn-ghost btn-sm btn-square rounded-btn"
      >
        <Icon icon="material-symbols:home-outline-rounded" class="size-6" />
      </a>
    </div>

    <div class="tooltip tooltip-bottom" data-tip="Comments (C)">
      <button
        onclick={() =>
          document
            .getElementById("comments")
            ?.scrollIntoView({ behavior: "smooth" })}
        class="btn btn-ghost btn-sm btn-square rounded-btn"
      >
        <Icon icon="iconamoon:comment" class="size-6" />
      </button>
    </div>

    <div class="tooltip tooltip-bottom" data-tip="Table of Contents (T)">
      <button onclick={openTOC} class="btn btn-outline btn-sm rounded-btn">
        <Icon icon="lucide:table-of-contents" class="size-5" />
        <span class="hidden sm:inline">Contents</span>
      </button>
    </div>

    <div class="tooltip tooltip-bottom" data-tip="Edit (E)">
      <button
        onclick={openEdit}
        class="btn btn-ghost btn-sm btn-square rounded-btn"
      >
        <Icon icon="material-symbols:edit-outline-rounded" class="size-6" />
      </button>
    </div>

    <div class="tooltip tooltip-bottom" data-tip="Settings (S)">
      <button
        onclick={openSettings}
        class="btn btn-ghost btn-sm btn-square rounded-btn"
      >
        <Icon icon="material-symbols:settings-outline-rounded" class="size-6" />
      </button>
    </div>
  </nav>
{:else}
  <button
    class="fixed top-4 right-4 z-50 btn btn-circle btn-ghost bg-base-100 shadow-md"
    onclick={() => (prefs.config.navbarVisible = true)}
  >
    <Icon icon="material-symbols:menu-rounded" class="size-6" />
  </button>
{/if}

<dialog bind:this={modals.chapter} class="modal modal-bottom sm:modal-middle">
  <div
    class="modal-box bg-base-100 p-0 rounded-t-2xl sm:rounded-box max-h-[80vh] flex flex-col"
  >
    <div
      class="sticky top-0 z-10 bg-base-100/95 backdrop-blur border-b border-base-content/10 p-4 space-y-3"
    >
      <div class="flex justify-between items-center">
        <h3 class="font-bold text-lg text-primary">Contents</h3>
        <form method="dialog">
          <button class="btn btn-sm btn-circle btn-ghost">✕</button>
        </form>
      </div>
      <div class="flex gap-2">
        <input
          type="search"
          bind:value={navState.searchQuery}
          placeholder="Search..."
          class="input input-bordered input-sm grow rounded-btn focus:input-primary"
        />
        <select
          class="select select-bordered select-sm rounded-btn focus:select-primary"
          bind:value={navState.selectedTL}
        >
          {#each Object.keys(bookData[bookSlug] || {}) as tl}
            <option value={tl}>{tl.toUpperCase()}</option>
          {/each}
        </select>
      </div>
    </div>

    <div class="overflow-y-auto p-2">
      {#each chapterList as ch}
        <a
          href="/read/{bookSlug}/{navState.selectedTL}/{ch.slug}"
          class="btn btn-sm justify-start w-full font-normal border-none mb-1 rounded-btn {readerState
            .ch_meta.slug == ch.slug
            ? 'btn-primary btn-soft'
            : 'btn-ghost'}"
          onclick={() => modals.chapter?.close()}
        >
          <span class="w-10 font-mono text-xs opacity-50">#{ch.slug}</span>
          <span class="truncate">{ch.title}</span>
        </a>
      {/each}
    </div>
  </div>
  <form method="dialog" class="modal-backdrop"><button>close</button></form>
</dialog>

<dialog bind:this={modals.settings} class="modal sm:modal-middle modal-bottom">
  <div class="modal-box bg-base-100 rounded-box">
    <div
      class="flex justify-between items-center mb-6 border-b border-base-content/10 pb-4"
    >
      <h3 class="font-bold text-lg flex items-center gap-2 text-primary">
        <Icon icon="material-symbols:settings-outline-rounded" /> Settings
      </h3>
      <div class="flex gap-2">
        <button
          class="btn btn-xs btn-ghost text-error rounded-btn"
          onclick={() => prefs.reset()}>Reset</button
        >
        <form method="dialog">
          <button class="btn btn-sm btn-circle btn-ghost">✕</button>
        </form>
      </div>
    </div>

    <div class="grid md:grid-cols-2 gap-8">
      <div class="space-y-4">
        <h4 class="text-xs font-bold opacity-50 uppercase tracking-widest">
          Appearance
        </h4>

        <div class="form-control">
          <label class="label"><span class="label-text">Theme</span></label>
          <select
            class="select select-bordered select-sm w-full rounded-btn focus:select-primary"
            bind:value={prefs.config.theme}
          >
            <optgroup label="Recommended">
              {#each PRIORITY_THEMES as t}
                <option value={t}
                  >{t.charAt(0).toUpperCase() + t.slice(1)}</option
                >
              {/each}
            </optgroup>
            <optgroup label="Other Themes">
              {#each MISC_THEMES as t}
                <option value={t}
                  >{t.charAt(0).toUpperCase() + t.slice(1)}</option
                >
              {/each}
            </optgroup>
          </select>
        </div>

        <div class="form-control">
          <label class="label"><span class="label-text">Font</span></label>
          <select
            class="select select-bordered select-sm w-full rounded-btn focus:select-primary"
            bind:value={prefs.config.font}
          >
            <optgroup label="Book Fonts">
              {#each BOOK_FONTS as f}
                <option value={f} style="font-family: {f}">{f}</option>
              {/each}
            </optgroup>
            <optgroup label="System Fonts">
              {#each SYSTEM_FONTS as f}
                <option value={f} style="font-family: {f}">{f}</option>
              {/each}
            </optgroup>
          </select>
        </div>

        <div class="form-control">
          <label class="label cursor-pointer justify-start gap-3">
            <input
              type="checkbox"
              class="toggle toggle-primary toggle-sm"
              bind:checked={prefs.config.solidBackground}
            />
            <span class="label-text">Solid Background</span>
          </label>
        </div>
      </div>

      <div class="space-y-4">
        <h4 class="text-xs font-bold opacity-50 uppercase tracking-widest">
          Readability
        </h4>
        <div class="grid grid-cols-2 gap-4">
          <div class="form-control">
            <label class="label text-xs">Size ({prefs.config.fontSize}px)</label
            >
            <input
              type="range"
              min="12"
              max="32"
              class="range range-xs range-primary"
              bind:value={prefs.config.fontSize}
            />
          </div>
          <div class="form-control">
            <label class="label text-xs"
              >Height ({prefs.config.lineHeight})</label
            >
            <input
              type="range"
              min="1.2"
              max="2.5"
              step="0.1"
              class="range range-xs range-secondary"
              bind:value={prefs.config.lineHeight}
            />
          </div>
        </div>
        <div class="form-control">
          <label class="label text-xs">Weight ({prefs.config.fontWeight})</label
          >
          <input
            type="range"
            min="300"
            max="900"
            step="25"
            class="range range-xs range-accent"
            bind:value={prefs.config.fontWeight}
          />
        </div>
        <div class="join w-full">
          {#each ["left", "center", "right", "justify"] as align}
            <button
              class="join-item btn btn-xs grow {prefs.config.textAlign === align
                ? 'btn-primary'
                : 'btn-ghost bg-base-200'}"
              onclick={() => (prefs.config.textAlign = align)}
            >
              <Icon icon="material-symbols:format-align-{align}" />
            </button>
          {/each}
        </div>
        <div class="flex flex-col gap-1 pt-2">
          <div class="form-control">
            <label class="label cursor-pointer justify-start gap-3">
              <input
                type="checkbox"
                class="toggle toggle-primary toggle-sm"
                bind:checked={prefs.config.indent}
              />
              <span class="label-text">Indent Paragraphs</span>
            </label>
          </div>
          <div class="form-control">
            <label class="label cursor-pointer justify-start gap-3">
              <input
                type="checkbox"
                class="toggle toggle-secondary toggle-sm"
                bind:checked={prefs.config.hyphens}
              />
              <span class="label-text">Auto-Hyphenation</span>
            </label>
          </div>
        </div>

        <div class="divider my-2"></div>
        <h4 class="text-xs font-bold opacity-50 uppercase tracking-widest">
          Interface
        </h4>

        <button
          class="btn btn-outline btn-primary btn-sm w-full rounded-btn"
          onclick={toggleFullscreen}
        >
          <Icon icon="material-symbols:fullscreen" class="size-5" /> Toggle Fullscreen
        </button>

        <div class="flex flex-col gap-1">
          <div class="form-control">
            <label class="label cursor-pointer justify-start gap-3">
              <input
                type="checkbox"
                class="toggle toggle-sm toggle-accent"
                bind:checked={prefs.config.navbarSticky}
              />
              <span class="label-text">Sticky Navbar</span>
            </label>
          </div>
          <div class="form-control">
            <label class="label cursor-pointer justify-start gap-3">
              <input
                type="checkbox"
                class="toggle toggle-sm toggle-accent"
                bind:checked={prefs.config.navbarVisible}
              />
              <span class="label-text">Show Navbar</span>
            </label>
          </div>
          <div class="form-control">
            <label class="label cursor-pointer justify-start gap-3">
              <input
                type="checkbox"
                class="toggle toggle-sm toggle-accent"
                bind:checked={prefs.config.showBottomBanner}
              />
              <span class="label-text">Info Banner</span>
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
  <form method="dialog" class="modal-backdrop"><button>close</button></form>
</dialog>

<dialog bind:this={modals.edit} class="modal modal-bottom sm:modal-middle">
  <div class="modal-box bg-base-100 rounded-box">
    <form method="dialog">
      <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
        >✕</button
      >
    </form>
    <h3 class="font-bold text-lg mb-4 text-primary">Contribute</h3>
    <div class="flex flex-col gap-3">
      <a
        href="https://github.com/Bittu5134/LOTM-Reader"
        target="_blank"
        class="btn btn-outline btn-primary w-full rounded-btn"
      >
        <Icon icon="mdi:book-open-page-variant" class="size-5 mr-2" /> Read Guide
      </a>
      <a
        href="https://github.com/Bittu5134/LOTM-Reader/tree/main/src/lib/data"
        target="_blank"
        class="btn btn-secondary w-full rounded-btn"
      >
        <Icon icon="mdi:github" class="size-5 mr-2" /> Repository
      </a>
    </div>
  </div>
  <form method="dialog" class="modal-backdrop"><button>close</button></form>
</dialog>
