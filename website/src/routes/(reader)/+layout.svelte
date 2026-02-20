<script lang="ts">
  import "../../app.css";
  import { onMount, onDestroy } from "svelte";
  import { browser } from "$app/environment";
  import { page } from "$app/state";
  import { goto, afterNavigate } from "$app/navigation";
  import Icon from "@iconify/svelte";
  import Giscus from "@giscus/svelte";

  // Components
  import Navbar from "$lib/reader/Navbar.svelte";
  import InfoBanner from "$lib/reader/InfoBanner.svelte";

  // Data
  import { readerState } from "$lib/reader.svelte.ts";
  import bookData from "$lib/meta.json";

  let { children } = $props();

  // --- Logic: User Preferences ---
  class UserPreferences {
    config = $state({
      theme: "sunset",
      font: "Alegreya",
      fontSize: 25,
      fontWeight: 450,
      lineHeight: 1.8,
      textAlign: "justify",
      hyphens: false,
      indent: false,
      navbarVisible: true,
      navbarSticky: true,
      showBottomBanner: true,
      solidBackground: true,
    });

    constructor() {
      if (browser) {
        this.load();
        $effect(() => {
          localStorage.setItem("readerSettings", JSON.stringify(this.config));
          document.documentElement.setAttribute(
            "data-theme",
            this.config.theme,
          );
        });
      }
    }

    load() {
      const saved = localStorage.getItem("readerSettings");
      if (saved) this.config = { ...this.config, ...JSON.parse(saved) };
      document.documentElement.setAttribute("data-theme", this.config.theme);
    }

    reset() {
      if (confirm("Reset settings?")) {
        this.config = {
          theme: "sunset",
          font: "Alegreya",
          fontSize: 25,
          fontWeight: 450,
          lineHeight: 1.8,
          textAlign: "justify",
          hyphens: false,
          indent: false,
          navbarVisible: true,
          navbarSticky: true,
          showBottomBanner: true,
          solidBackground: true,
        };
      }
    }
  }

  function getGiscusTheme(daisyTheme: string) {
    const themeMapping: Record<string, string> = {
      light: "light_tritanopia",
      cupcake: "light_tritanopia",
      bumblebee: "light_tritanopia",
      emerald: "light_tritanopia",
      corporate: "light_tritanopia",
      valentine: "light_tritanopia",
      garden: "light_tritanopia",
      fantasy: "light_tritanopia",
      cmyk: "light_tritanopia",
      autumn: "light_tritanopia",
      acid: "catppuccin_latte",
      lemonade: "light_tritanopia",
      winter: "light_tritanopia",
      lofi: "noborder_light",
      wireframe: "light_high_contrast",
      pastel: "catppuccin_latte",
      retro: "gruvbox_light",
      coffee: "gruvbox_dark",
      dark: "dark_dimmed",
      black: "fro",
      luxury: "noborder_dark",
      business: "noborder_gray",
      night: "cobalt",
      dim: "dark_dimmed",
      nord: "light_tritanopia",
      sunset: "noborder_dark",
      dracula: "purple_dark",
      synthwave: "purple_dark",
      cyberpunk: "gruvbox_light",
      aqua: "cobalt",
      forest: "noborder_dark",
      halloween: "gruvbox",
    };

    return themeMapping[daisyTheme] || "dark";
  }

  // --- State ---
  const prefs = new UserPreferences();
  let mainContainer: HTMLDivElement;
  let navbarRef: any;

  // 1. Parse URL manually (since page.params is empty)
  // Split path, filter out empty strings to handle trailing slashes
  // URL: /read/coi/webnovel/1 -> ["read", "coi", "webnovel", "1"]
  const pathSegments = $derived(page.url.pathname.split("/").filter(Boolean));

  // 2. Derive values from URL position
  const bookSlug = $derived(pathSegments[1] ?? "lotm");
  const currentTL = $derived(pathSegments[2] ?? "webnovel");
  const currentChapter = $derived(Number(pathSegments[3]) || 1);
  let githubID = $derived(readerState.ch_meta.discussion || 1);

  // 3. Get Total Chapters for the current TL
  const totalChapters = $derived(
    bookData[bookSlug][currentTL].length
  );
  console.log(totalChapters)

  let navState = $state({ searchQuery: "", selectedTL: "webnovel" });

  // 4. Sync internal state with URL
  $effect(() => {
    navState.selectedTL = currentTL;
  });

  // --- Handlers ---

  afterNavigate(async () => {
    const { littlefoot } = await import("littlefoot");
    littlefoot({
      activateOnHover: true,
      hoverDelay: 50,
      dismissOnUnhover: true,
      buttonTemplate: `<button aria-label="Footnote <% number %>" class="relative btn btn-xs btn-info px-3 py-2 h-3 text-sm mx-1 font-mono"><% number %></button>`,
    });
  });
  onMount(async () => {
    if (browser) {
      const lastRead = JSON.parse(localStorage.getItem("lastRead") || "{} ");
      // Check if saved position matches current URL
      if (lastRead.slug == currentChapter && lastRead.book === bookSlug) {
        window.scrollTo({ top: lastRead.scroll, behavior: "instant" });
      }
      window.addEventListener("scroll", handleScroll);
    }
  });

  onDestroy(() => {
    if (browser) window.removeEventListener("scroll", handleScroll);
  });

  function handleScroll() {
    localStorage.setItem(
      "lastRead",
      JSON.stringify({
        book: bookSlug,
        tl: currentTL,
        slug: currentChapter,
        scroll: window.scrollY,
        timestamp: Date.now(),
      }),
    );
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(console.error);
    } else {
      document.exitFullscreen();
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (["INPUT", "TEXTAREA"].includes((event.target as HTMLElement).tagName))
      return;

    // Use derived URL chapter for navigation
    const slug = currentChapter;
    const key = event.key.toLowerCase();

    switch (key) {
      case "h":
        goto(`/book/${bookSlug}`);
        break;
      case "e":
        navbarRef?.openEdit();
        break;
      case "t":
        navbarRef?.openTOC();
        break;
      case "s":
        navbarRef?.openSettings();
        break;
      case "c":
        document
          .getElementById("comments")
          ?.scrollIntoView({ behavior: "smooth" });
        break;
      case "f":
        toggleFullscreen();
        break;
      case "n":
      case "arrowright":
         // Check if it's the last chapter before navigating
         if (slug < totalChapters) {
            goto(`/read/${bookSlug}/${currentTL}/${slug + 1}`);
         }
        break;
      case "p":
      case "arrowleft":
        if (slug > 1) {
            goto(`/read/${bookSlug}/${currentTL}/${slug - 1}`);
        }
        break;
    }
  }
</script>

<svelte:window onkeydown={handleKeydown} />

<div
  bind:this={mainContainer}
  class="min-h-screen w-full bg-base-100 text-base-content relative transition-colors duration-200"
  style="
    --chapter-font: {prefs.config.font}, serif; 
    --chapter-size: {prefs.config.fontSize}px; 
    --chapter-weight: {prefs.config.fontWeight};
    --chapter-lh: {prefs.config.lineHeight};
    --chapter-indent: {prefs.config.indent ? '1.5em' : '0'};
    --chapter-align: {prefs.config.textAlign};
    --chapter-hyphens: {prefs.config.hyphens ? 'auto' : 'none'};
    --card-bg-opacity: {prefs.config.solidBackground ? 1 : 0};
  "
>
  <Navbar bind:this={navbarRef} {prefs} {bookSlug} {bookData} bind:navState />

  <main class="mx-auto my-3 max-w-4xl w-full px-6 py-12 md:px-12 z-0 relative">
    <div
      class="absolute inset-0 bg-base-200 -z-10 rounded-box transition-opacity duration-300"
      style="opacity: var(--card-bg-opacity);"
    ></div>

    <article
      class="chapter-content prose prose-lg md:prose-xl max-w-none wrap-break-word"
    >
      {@render children()}
    </article>

    <div class="mt-16 flex items-center justify-between border-t border-base-content/10 pt-8">
      <a
        href={currentChapter <= 1 
            ? `/book/${bookSlug}` 
            : `/read/${bookSlug}/${navState.selectedTL}/${currentChapter - 1}`}
        class="btn btn-soft btn-sm gap-2"
        aria-label={currentChapter <= 1 ? "Go Home" : "Previous Chapter"}
      >
        <Icon icon={currentChapter <= 1 ? "iconamoon:home-light" : "mage:previous"} class="size-5" />
        <span class="hidden sm:inline">{currentChapter <= 1 ? "Home" : "Prev"}</span>
      </a>

      <span class="text-xs font-mono font-bold opacity-50 tracking-wider">
        CH. {readerState.ch_meta.slug}
      </span>

      <a
        href={currentChapter >= totalChapters
            ? `/book/${bookSlug}`
            : `/read/${bookSlug}/${navState.selectedTL}/${currentChapter + 1}`}
        class="btn btn-soft btn-sm gap-2"
        aria-label={currentChapter >= totalChapters ? "Go Home" : "Next Chapter"}
      >
        <span class="hidden sm:inline">{currentChapter >= totalChapters ? "Home" : "Next"}</span>
        <Icon icon={currentChapter >= totalChapters ? "iconamoon:home-light" : "mage:next"} class="size-5" />
      </a>
    </div>
  </main>

  {#if prefs.config.showBottomBanner}
    <InfoBanner />
  {/if}

  <div id="comments" class="sm:mx-auto mx-0 max-w-5xl sm:px-6 px-3 pb-6 scroll-mt-20">
    <Giscus
      id="comments"
      repo="bittu5134/lotm-reader"
      repoId="R_kgDORObHsw"
      category={bookSlug.toUpperCase()}
      categoryId={bookSlug === "LOTM"
        ? "DIC_kwDORObHs84C2RKd"
        : "DIC_kwDORObHs84C2RKe"}
      mapping="number"
      term={String(githubID)}
      reactionsEnabled="1"
      emitMetadata="0"
      inputPosition="top"
      theme={getGiscusTheme(prefs.config.theme)}
      lang="en"
      loading="lazy"
    />
  </div>
</div>

<style>
  .chapter-content {
    font-family: var(--chapter-font);
    font-size: var(--chapter-size);
    line-height: var(--chapter-lh);
    text-align: var(--chapter-align);
    hyphens: var(--chapter-hyphens);
    font-weight: var(--chapter-weight, 400);
  }

  .chapter-content :global(p) {
    text-indent: var(--chapter-indent);
  }

  :global(:fullscreen) {
    width: 100vw;
    height: 100vh;
    overflow-y: auto;
    overflow-x: hidden;
    background-color: var(--fallback-b1, oklch(var(--b1) / 1));
  }
</style>