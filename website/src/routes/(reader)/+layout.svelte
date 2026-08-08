<script lang="ts">
  import "../../app.css";
  import { onMount, onDestroy, tick } from "svelte";
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
      showComments: true,
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
          showComments: true,
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

  // --- Giscus Lazy Loading & Error Mitigation State ---
  let giscusLoggedIn = $state<boolean>(
    browser ? localStorage.getItem("giscusLoggedIn") === "true" : false,
  );
  let commentsOpen = $state<boolean>(false);
  let commentCount = $state<number | null>(null);
  let giscusStatus = $state<"idle" | "loading" | "success" | "error">("idle");
  let giscusTimeoutId: any = null;

  function revealComments() {
    commentsOpen = true;
    giscusStatus = "loading";
    startGiscusTimeout();
  }

  function startGiscusTimeout() {
    if (giscusTimeoutId) clearTimeout(giscusTimeoutId);
    giscusTimeoutId = setTimeout(() => {
      if (giscusStatus === "loading") {
        console.warn(`[Giscus] Timeout check for discussion ${githubID}`);
        // Only set error if still in loading state after 12s without any Giscus message
        giscusStatus = "error";
      }
    }, 12000);
  }

  async function fetchCommentCount(id: number) {
    if (!id || id <= 0) return;
    try {
      const res = await fetch(
        `https://api.github.com/repos/bittu5134/lotm-reader/discussions/${id}`
      );
      if (!res.ok) return;
      const data = await res.json();
      if (typeof data.comments === "number" && data.comments > 0) {
        commentCount = data.comments;
      } else {
        commentCount = 0;
      }
    } catch (err) {
      console.warn("[Giscus] Failed to fetch comments count:", err);
    }
  }

  // Listen for Giscus postMessages and custom events
  $effect(() => {
    if (!browser) return;

    const handleMessage = (event: MessageEvent) => {
      if (event.origin !== "https://giscus.app") return;
      const giscusData = event.data?.giscus;
      if (!giscusData) return;

      if ("error" in giscusData) {
        console.warn("[Giscus] Error reported:", giscusData.error);
        giscusStatus = "error";
        giscusLoggedIn = false;
        localStorage.setItem("giscusLoggedIn", "false");
        if (giscusTimeoutId) {
          clearTimeout(giscusTimeoutId);
          giscusTimeoutId = null;
        }
      } else {
        // Any non-error message from giscus.app (viewer, discussion, resize, etc.) confirms comments loaded
        giscusStatus = "success";
        if (giscusTimeoutId) {
          clearTimeout(giscusTimeoutId);
          giscusTimeoutId = null;
        }

        if ("viewer" in giscusData) {
          const username = giscusData.viewer?.login;
          const isLoggedIn =
            typeof username === "string" &&
            username.trim() !== "" &&
            username !== "null" &&
            username !== "undefined" &&
            username !== "giscus[bot]";

          giscusLoggedIn = isLoggedIn;
          localStorage.setItem("giscusLoggedIn", String(isLoggedIn));
        }
      }
    };

    const handleOpenComments = () => {
      if (!commentsOpen) {
        revealComments();
      }
    };

    const handleLinkClick = (e: MouseEvent) => {
      const target = (e.target as HTMLElement).closest("a");
      if (target && target.getAttribute("href") === "#comments") {
        if (!commentsOpen) {
          revealComments();
        }
      }
    };

    window.addEventListener("message", handleMessage);
    window.addEventListener("open-comments", handleOpenComments);
    window.addEventListener("click", handleLinkClick);

    return () => {
      window.removeEventListener("message", handleMessage);
      window.removeEventListener("open-comments", handleOpenComments);
      window.removeEventListener("click", handleLinkClick);
    };
  });

  // Watch for navigation/chapter changes to decide auto-open vs lazy load button
  $effect(() => {
    if (!prefs.config.showComments) return;

    const id = githubID;
    const slug = bookSlug;

    if (browser) {
      const urlParams = page.url.searchParams;
      const hasCommentsParam = urlParams.has("comments");
      const hasGiscusParam = urlParams.has("giscus");
      const hasCodeParam = urlParams.has("code");
      const isHashComments = page.url.hash === "#comments";

      const storedLogin = localStorage.getItem("giscusLoggedIn") === "true";
      giscusLoggedIn = storedLogin;

      const forceOpen =
        storedLogin ||
        hasCommentsParam ||
        hasGiscusParam ||
        hasCodeParam ||
        isHashComments;

      if (forceOpen) {
        commentsOpen = true;
        giscusStatus = "loading";

        // Remove ?comments=1 parameter immediately from address bar to keep URL clean
        if (hasCommentsParam) {
          urlParams.delete("comments");
          const newSearch = urlParams.toString();
          const newUrl =
            window.location.pathname +
            (newSearch ? "?" + newSearch : "") +
            window.location.hash;
          window.history.replaceState({}, "", newUrl);
        }

        startGiscusTimeout();
      } else {
        commentsOpen = false;
        giscusStatus = "idle";
        commentCount = null;
        fetchCommentCount(id);
      }
    }

    return () => {
      if (giscusTimeoutId) {
        clearTimeout(giscusTimeoutId);
        giscusTimeoutId = null;
      }
    };
  });

  // 1. Parse URL manually (since page.params is empty)
  const pathSegments = $derived(page.url.pathname.split("/").filter(Boolean));

  // 2. Derive values from URL position
  const bookSlug = $derived(pathSegments[1] ?? "lotm");
  const currentTL = $derived(pathSegments[2] ?? "webnovel");
  const currentChapter = $derived(Number(pathSegments[3]) || 1);

  // Derive chapter metadata directly from meta.json based on URL (ensuring SSR & crawler accuracy)
  const currentChapterMeta = $derived.by(() => {
    const chapters = (bookData as any)[bookSlug]?.[currentTL];
    if (!Array.isArray(chapters)) return null;

    const idx = currentChapter - 1;
    if (chapters[idx] && Number(chapters[idx].slug) === currentChapter) {
      return chapters[idx];
    }
    return chapters.find((ch: any) => Number(ch.slug) === currentChapter) || chapters[idx] || null;
  });

  const chapterSlug = $derived(currentChapterMeta?.slug ?? readerState.ch_meta.slug ?? currentChapter);
  const chapterTitle = $derived(currentChapterMeta?.title || readerState.ch_meta.title || "");
  const githubID = $derived(currentChapterMeta?.discussion || readerState.ch_meta.discussion || 1);

  // 3. Get Total Chapters for the current TL
  const totalChapters = $derived(
    (bookData as any)[bookSlug]?.[currentTL]?.length ?? 1
  );

  let navState = $state({ searchQuery: "", selectedTL: "webnovel" });

  // 4. Sync internal state with URL
  $effect(() => {
    navState.selectedTL = currentTL;
  });

  function readerPathId(url: URL): string | null {
    const p = url.pathname.replace(/\/$/, "").split("/").filter(Boolean);
    if (p[0] !== "read" || p.length < 4) return null;
    return `${p[1]}/${p[2]}/${p[3]}`;
  }

  async function scrollReaderToTop() {
    await tick();

    requestAnimationFrame(() => {
      window.scrollTo({
        top: 0,
        left: 0,
        behavior: "auto",
      });
    });
  }

  // --- Handlers ---

  afterNavigate(async ({ from, to }) => {
    const { littlefoot } = await import("littlefoot");
    littlefoot({
      activateOnHover: true,
      hoverDelay: 50,
      dismissOnUnhover: true,
      buttonTemplate: `<button aria-label="Footnote <% number %>" class="relative btn btn-xs btn-info px-3 py-2 h-3 text-sm mx-1 font-mono"><% number %></button>`,
    });

    if (!browser || !from || !to) return;

    const prevId = readerPathId(from.url);
    const nextId = readerPathId(to.url);
    // When loading a new chapter ensure reader scrolls to top of page
    if (prevId && nextId && prevId !== nextId) {
      await scrollReaderToTop();
    }
  });

  onMount(async () => {
    if (browser) {
      const lastRead = JSON.parse(localStorage.getItem("lastRead") || "{}");
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
        if (!commentsOpen) {
          revealComments();
        }
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
          goto(`/read/${bookSlug}/${currentTL}/${slug + 1}${commentsOpen ? '?comments=1' : ''}`);
        }
        break;
      case "p":
      case "arrowleft":
        if (slug > 1) {
          goto(`/read/${bookSlug}/${currentTL}/${slug - 1}${commentsOpen ? '?comments=1' : ''}`);
        }
        break;
    }
  }
</script>

<svelte:head>
  <title>{bookSlug.toUpperCase()} {chapterSlug}{chapterTitle ? ` — ${chapterTitle}` : ""}</title>
  <meta name="description" content={`Read ${bookSlug.toUpperCase()} Chapter ${chapterSlug}${chapterTitle ? `: ${chapterTitle}` : ""} online.`} />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="LOTM Reader" />
  <meta property="og:title" content="{bookSlug.toUpperCase()} {chapterSlug}{chapterTitle ? ` — ${chapterTitle}` : ""}" />
  <meta property="og:description" content={`Read ${bookSlug.toUpperCase()} Chapter ${chapterSlug}${chapterTitle ? `: ${chapterTitle}` : ""} online.`} />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{bookSlug.toUpperCase()} {chapterSlug}{chapterTitle ? ` — ${chapterTitle}` : ""}" />
  <meta name="twitter:description" content={`Read ${bookSlug.toUpperCase()} Chapter ${chapterSlug}${chapterTitle ? `: ${chapterTitle}` : ""} online.`} />
</svelte:head>

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
            : `/read/${bookSlug}/${navState.selectedTL}/${currentChapter - 1}${commentsOpen ? '?comments=1' : ''}`}
        class="btn btn-soft btn-sm gap-2"
        aria-label={currentChapter <= 1 ? "Go Home" : "Previous Chapter"}
      >
        <Icon icon={currentChapter <= 1 ? "iconamoon:home-light" : "mage:previous"} class="size-5" />
        <span class="hidden sm:inline">{currentChapter <= 1 ? "Home" : "Prev"}</span>
      </a>

      <span class="text-xs font-mono font-bold opacity-50 tracking-wider">
        CH. {chapterSlug}
      </span>

      <a
        href={currentChapter >= totalChapters
            ? `/book/${bookSlug}`
            : `/read/${bookSlug}/${navState.selectedTL}/${currentChapter + 1}${commentsOpen ? '?comments=1' : ''}`}
        class="btn btn-soft btn-sm gap-2"
        aria-label={currentChapter >= totalChapters ? "Go Home" : "Next Chapter"}
        data-sveltekit-preload-data="viewport"
      >
        <span class="hidden sm:inline">{currentChapter >= totalChapters ? "Home" : "Next"}</span>
        <Icon icon={currentChapter >= totalChapters ? "iconamoon:home-light" : "mage:next"} class="size-5" />
      </a>
    </div>
  </main>

  {#if prefs.config.showBottomBanner}
    <InfoBanner />
  {/if}

  {#if prefs.config.showComments}
  <div id="comments" class="sm:mx-auto mx-0 max-w-4xl sm:px-6 px-3 pb-8 scroll-mt-20">
    {#if !commentsOpen}
      <div id="show-discussion-container" class="my-6 text-center max-w-xl mx-auto px-2">
        <button
          id="show-discussion-btn"
          onclick={() => revealComments()}
          class="w-full sm:w-auto min-w-[280px] min-h-[56px] py-4 px-8 btn btn-primary rounded-xl font-bold text-base md:text-lg shadow-md hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 flex items-center justify-center gap-3 mx-auto cursor-pointer"
        >
          <Icon icon="iconamoon:comment-bold" class="size-6" />
          <span>
            {commentCount !== null && commentCount > 0
              ? `Show Comments (${commentCount})`
              : "Show Comments"}
          </span>
        </button>
      </div>
    {:else}
      {#if giscusStatus === "error"}
        <div class="card bg-warning/10 border-2 border-warning/40 text-base-content shadow-xl p-6 md:p-8 rounded-2xl my-6 max-w-2xl mx-auto text-center flex flex-col items-center justify-center gap-4 transition-all duration-200">
          <div class="p-3 bg-warning/20 text-warning rounded-full">
            <Icon icon="heroicons:exclamation-triangle-solid" class="size-9" />
          </div>
          <div class="space-y-2 max-w-lg mx-auto text-center">
            <h3 class="text-xl md:text-2xl font-bold text-warning tracking-wide">
              Comments Rate Limit Exceeded
            </h3>
            <p class="text-sm md:text-base opacity-90 leading-relaxed font-medium">
              GitHub Giscus rate limit has been reached for anonymous requests. Log in with your GitHub account to use your personal quota, or open the discussion page directly:
            </p>
          </div>
          <div class="mt-2 flex flex-col sm:flex-row flex-wrap gap-3 justify-center items-center w-full max-w-md mx-auto">
            <a
              href={`https://giscus.app/api/oauth/authorize?redirect_uri=${encodeURIComponent(
                browser ? window.location.href : ""
              )}#comments`}
              class="w-full sm:w-auto min-h-[52px] py-3.5 px-6 btn btn-warning rounded-xl text-base font-bold flex items-center justify-center gap-2 shadow-md hover:scale-[1.02] active:scale-95 transition-all"
            >
              <Icon icon="material-symbols:login-rounded" class="size-5" />
              <span>Log In to View Comments</span>
            </a>
            <a
              href={`https://github.com/bittu5134/lotm-reader/discussions/${githubID}`}
              target="_blank"
              rel="noopener noreferrer"
              class="w-full sm:w-auto min-h-[52px] py-3.5 px-6 btn btn-outline btn-warning rounded-xl text-base font-bold flex items-center justify-center gap-2 hover:scale-[1.02] active:scale-95 transition-all"
            >
              <Icon icon="material-symbols:open-in-new" class="size-5" />
              <span>Open Discussion Page</span>
            </a>
          </div>
        </div>
      {:else if !giscusLoggedIn}
        <div class="card bg-base-200/80 border border-primary/20 text-base-content shadow-sm p-4 md:p-5 rounded-2xl mb-6 max-w-2xl mx-auto text-center flex flex-col sm:flex-row items-center justify-between gap-4 transition-all duration-200">
          <div class="flex items-center gap-3 text-left">
            <div class="p-2.5 bg-primary/10 text-primary rounded-xl flex-shrink-0">
              <Icon icon="iconamoon:info-circle-bold" class="size-6" />
            </div>
            <div>
              <h4 class="text-sm md:text-base font-bold">Having trouble loading comments?</h4>
              <p class="text-xs md:text-sm opacity-75">Log in via GitHub or open the discussion page directly.</p>
            </div>
          </div>
          <div class="flex flex-col sm:flex-row gap-2.5 w-full sm:w-auto flex-shrink-0">
            <a
              href={`https://giscus.app/api/oauth/authorize?redirect_uri=${encodeURIComponent(
                browser ? window.location.href : ""
              )}#comments`}
              class="min-h-[48px] py-3 px-5 btn btn-primary rounded-xl text-xs md:text-sm font-bold flex items-center justify-center gap-1.5 shadow-sm hover:scale-[1.02] active:scale-95 transition-all"
            >
              <Icon icon="material-symbols:login-rounded" class="size-5" />
              <span>Log In</span>
            </a>
            <a
              href={`https://github.com/bittu5134/lotm-reader/discussions/${githubID}`}
              target="_blank"
              rel="noopener noreferrer"
              class="min-h-[48px] py-3 px-5 btn btn-outline btn-primary rounded-xl text-xs md:text-sm font-bold flex items-center justify-center gap-1.5 hover:scale-[1.02] active:scale-95 transition-all"
            >
              <Icon icon="material-symbols:open-in-new" class="size-5" />
              <span>Open Discussion</span>
            </a>
          </div>
        </div>
      {/if}

      {#if giscusStatus !== "error"}
        <div>
          <Giscus
            id="comments-giscus"
            repo="bittu5134/lotm-reader"
            repoId="R_kgDORObHsw"
            category={bookSlug.toUpperCase()}
            categoryId={bookSlug === "LOTM"
              ? "DIC_kwDORObHs84C2RKd"
              : "DIC_kwDORObHs84C2RKe"}
            mapping="number"
            term={String(githubID)}
            reactionsEnabled="1"
            emitMetadata="1"
            inputPosition="top"
            theme={getGiscusTheme(prefs.config.theme)}
            lang="en"
            loading="lazy"
          />
        </div>
      {/if}
    {/if}
  </div>
  {/if}
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