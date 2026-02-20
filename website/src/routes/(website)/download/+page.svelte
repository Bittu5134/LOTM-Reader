<script lang="ts">
  import Icon from "@iconify/svelte";
  import { fade, fly } from "svelte/transition";

  // --- Data Structure ---
  // PASTE YOUR REAL GITHUB LINKS BELOW
  const archives = {
    lotm: {
      title: "Lord of the Mysteries",
      id: "lotm",
      coverColor: "from-red-900/40 to-black/60",
      tls: [
        {
          name: "Webnovel Official",
          translator: "CKTalon",
          description:
            "The complete, polished official translation with community edits. Recommended for first-time readers.",
          downloads: {
            // Example: https://github.com/YourUser/YourRepo/releases/download/v1.0/lotm.epub
            standard: "https://github.com/Bittu5134/LOTM-Reader/releases/download/v1.0/lotm_webnovel_standard.epub",
            legacy: "https://github.com/Bittu5134/LOTM-Reader/releases/download/v1.0/lotm_webnovel_legacy.epub",
          },
        },
        {
          name: "Old Translation",
          translator: "CKTalon",
          description:
            "The original translation iteration. Kept for archival purposes.",
          downloads: {
            standard: "https://github.com/Bittu5134/LOTM-Reader/releases/download/v1.0/lotm_old_standard.epub",
            legacy: "https://github.com/Bittu5134/LOTM-Reader/releases/download/v1.0/lotm_old_legacy.epub",
          },
        },
      ],
    },
    coi: {
      title: "Circle of Inevitability",
      id: "coi",
      coverColor: "from-amber-900/40 to-black/60",
      tls: [
        {
          name: "Webnovel Official",
          translator: "CKTalon",
          description: "The ongoing sequel to Lord of the Mysteries.",
          downloads: {
            standard: "https://github.com/Bittu5134/LOTM-Reader/releases/download/v1.0/coi_webnovel_standard.epub",
            legacy: "https://github.com/Bittu5134/LOTM-Reader/releases/download/v1.0/coi_webnovel_legacy.epub",
          },
        },
      ],
    },
  };

  // State
  let selectedBook: "lotm" | "coi" = "lotm";

  // Helper to get active book data
  $: activeData = archives[selectedBook];
</script>

<div class="flex flex-col items-center justify-center min-h-dvh p-4 md:p-8">
  <div class="max-w-4xl w-full">
    <header class="text-center mb-12">
      <h1 class="text-3xl md:text-5xl font-bold mb-3 tracking-tight">
        Offline Archives
      </h1>
      <p class="text-base-content/60 max-w-lg mx-auto">
        Download the complete chronicles for offline reading. Choose the format
        that best suits your device.
      </p>
    </header>

    <div class="flex justify-center mb-8">
      <div
        class="bg-base-300/50 p-1 rounded-xl inline-flex gap-1 border border-white/5 backdrop-blur-sm"
      >
        <button
          class="px-6 py-2.5 rounded-lg text-sm font-bold transition-all duration-200 flex items-center gap-2
          {selectedBook === 'lotm'
            ? 'bg-primary text-primary-content shadow-md'
            : 'hover:bg-white/5 text-base-content/70'}"
          on:click={() => (selectedBook = "lotm")}
        >
          <Icon icon="game-icons:book-cover" class="size-5" />
          LOTM
        </button>
        <button
          class="px-6 py-2.5 rounded-lg text-sm font-bold transition-all duration-200 flex items-center gap-2
          {selectedBook === 'coi'
            ? 'bg-primary text-primary-content shadow-md'
            : 'hover:bg-white/5 text-base-content/70'}"
          on:click={() => (selectedBook = "coi")}
        >
          <Icon icon="game-icons:burning-book" class="size-5" />
          COI
        </button>
      </div>
    </div>

    {#key selectedBook}
      <div
        in:fly={{ y: 20, duration: 300, delay: 100 }}
        out:fade={{ duration: 150 }}
        class="grid gap-6"
      >
        {#each activeData.tls as tl}
          <div
            class="group relative overflow-hidden rounded-2xl border border-white/10 bg-base-200/40 shadow-xl transition-all hover:border-white/20 hover:shadow-2xl hover:bg-base-200/60"
          >
            <div
              class="absolute inset-0 bg-linear-to-br {activeData.coverColor} opacity-0 group-hover:opacity-10 transition-opacity duration-500"
            ></div>

            <div
              class="relative p-6 md:p-8 flex flex-col md:flex-row gap-8 items-start"
            >
              <div class="flex-1 space-y-3">
                <div class="flex items-center gap-3">
                  <span
                    class="badge badge-primary badge-outline font-mono text-xs font-bold tracking-widest"
                    >EPUB</span
                  >
                  {#if tl.name.includes("Official")}
                    <span
                      class="badge badge-success badge-soft text-xs font-bold"
                      >RECOMMENDED</span
                    >
                  {/if}
                </div>

                <h2 class="text-2xl font-bold text-white">{tl.name}</h2>
                <div
                  class="flex items-center gap-2 text-xs font-mono opacity-50 uppercase tracking-wider"
                >
                  <Icon icon="mdi:translate" class="size-4" />
                  <span>Trans. by {tl.translator}</span>
                </div>
                <p class="text-base-content/70 leading-relaxed text-sm pt-2">
                  {tl.description}
                </p>
              </div>

              <div class="w-full md:w-80 flex flex-col gap-3 shrink-0">
                <a
                  href={tl.downloads.standard}
                  target="_blank"
                  rel="noopener noreferrer"
                  class="btn h-auto py-3 px-4 border-none bg-linear-to-r from-primary/90 to-primary text-white hover:brightness-110 shadow-lg shadow-primary/20 flex items-center justify-between group/btn"
                >
                  <div class="text-left">
                    <div class="font-bold flex items-center gap-2">
                      Standard Edition
                      <Icon
                        icon="mdi:star-four-points"
                        class="size-3 text-yellow-300"
                      />
                    </div>
                    <div class="text-[10px] opacity-80 font-normal">
                      High-Res Images • Modern Styling
                    </div>
                  </div>
                  <Icon
                    icon="mdi:download"
                    class="size-6 opacity-70 group-hover/btn:translate-y-1 transition-transform"
                  />
                </a>

                <a
                  href={tl.downloads.legacy}
                  target="_blank"
                  rel="noopener noreferrer"
                  class="btn h-auto py-3 px-4 btn-outline border-base-content/20 hover:bg-base-content/5 hover:border-base-content/30 text-base-content flex items-center justify-between group/btn"
                >
                  <div class="text-left">
                    <div
                      class="font-bold flex items-center gap-2 text-base-content/90"
                    >
                      Legacy Edition
                      <Icon icon="mdi:e-reader" class="size-4 opacity-50" />
                    </div>
                    <div class="text-[10px] opacity-60 font-normal">
                      B&W Images • EPUB2 • Old Devices
                    </div>
                  </div>
                  <Icon
                    icon="mdi:download-outline"
                    class="size-6 opacity-40 group-hover/btn:translate-y-1 transition-transform"
                  />
                </a>
              </div>
            </div>
          </div>
        {/each}
      </div>
    {/key}

    <footer class="mt-16 text-center space-y-4">
      <p class="text-xs text-base-content/30 max-w-md mx-auto">
        Note: Files are hosted securely on GitHub. If you experience issues with
        the "Standard" version on older devices (Kindle PPW3 or older), please
        try the "Legacy" version.
      </p>
    </footer>
  </div>
</div>