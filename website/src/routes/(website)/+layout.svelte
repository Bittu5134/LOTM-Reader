<script lang="ts">
  import imgBG from "$lib/assets/web-bg.jpg?enhanced";
  import Icon from "@iconify/svelte";
  import "../../app.css";
  import { page } from "$app/state";
  import { goto } from "$app/navigation";
  import imgMeta from "$lib/assets/web-the-fool.jpg?url";

  let { children } = $props();

  let isHomePage = $derived(page.url.pathname === "/");

  function handleBack() {
    if (typeof window !== "undefined" && window.history.length > 1) {
      goto("../");
    } else {
      goto("/");
    }
  }
  $effect(() => {
    const _ = page.url.href;
    document.documentElement.setAttribute("data-theme", "sunset");
  });
</script>

<svelte:head>
  <title>LOTM-Reader</title>
  <meta
    name="description"
    content="The Fool that doesn’t belong to this era, the mysterious ruler above the gray fog..."
  />

  <meta property="og:type" content="website" />
  <meta property="og:title" content="LOTM-Reader" />
  <meta
    property="og:description"
    content="The Fool that doesn’t belong to this era, the mysterious ruler above the gray fog; the King of Yellow and Black who wields good luck…"
  />
  <meta property="og:image" content="http://beyonder.pages.dev{imgMeta}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="LOTM-Reader" />
  <meta
    name="twitter:description"
    content="The Fool that doesn’t belong to this era, the mysterious ruler above the gray fog; the King of Yellow and Black who wields good luck…"
  />
  <meta name="twitter:image" content="http://beyonder.pages.dev{imgMeta}" />
</svelte:head>

<div class="fixed inset-0 -z-10 overflow-hidden">
  <enhanced:img src={imgBG} alt="" class="w-full h-full object-cover" />

  <div class="absolute inset-0 bg-black/50 backdrop-blur-xs"></div>
</div>

{#if !isHomePage}
  <div class="fixed top-4 left-4 z-50">
    <button
      onclick={handleBack}
      class="btn btn-circle btn-ghost bg-base-300/50 backdrop-blur-md hover:bg-base-300 transition-all shadow-lg"
      aria-label="Go back"
    >
      <Icon icon="material-symbols:arrow-back-rounded" class="size-6" />
    </button>
  </div>
{/if}

{@render children()}
