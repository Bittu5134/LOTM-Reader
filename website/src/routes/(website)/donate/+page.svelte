<script lang="ts">
  import Icon from "@iconify/svelte";

  let btc = "bc1qu3vqcvfgzhwagpsyqcgcqs94vtymm6eagm2sw3";
  let eth = "0x9Ed0416c9083E836aB3C855e08b54BE77eff6c7B";
  let sol = "BEXMTBvrN9zC52LqR8rLxnMSWRhL52kSUiWx7ePnCDQE";

  async function copy(text: string, e: MouseEvent) {
    const target = e.currentTarget as HTMLElement;
    const originalText = target.innerText;
    await navigator.clipboard.writeText(text);
    target.innerText = "Copied to Clipboard!";
    setTimeout(() => (target.innerText = originalText), 1500);
  }
</script>

<div class="flex flex-col items-center justify-center min-h-dvh p-6">
  <div
    class="max-w-3xl w-full bg-base-300/40 backdrop-blur-xl border border-white/10 rounded-2xl p-8 shadow-2xl relative overflow-hidden"
  >
    <div class="absolute -top-10 -right-10 opacity-5 pointer-events-none">
      <Icon icon="game-icons:crystal-ball" class="size-64" />
    </div>

    <header class="text-center mb-8 relative z-10">
      <h1 class="text-4xl font-bold text-primary mb-2">
        Support <a href="/" class="hover:text-secondary transition-colors"
          >LOTM-Reader</a
        >
      </h1>
      <p class="text-base-content/70 italic text-sm">
        "Every small contribution helps us keep the lights on and the story
        alive for everyone."
      </p>
    </header>

    <div class="space-y-6 relative z-10">
      <section
        class="bg-base-200/50 p-6 rounded-xl border border-white/5 shadow-inner"
      >
        <div class="flex items-center gap-2 mb-4">
          <Icon icon="mdi:gift" class="text-secondary size-6" />
          <h2 class="text-xl font-semibold text-secondary">Donate</h2>
        </div>

        <ul class="space-y-3 text-sm">
          <li>
            <a
              href="https://www.eneba.com/store/eneba-gift-cards"
              target="_blank"
              class="flex items-center gap-2 hover:text-primary transition-colors font-bold"
            >
              <Icon icon="mdi:wallet" /> Eneba Wallet (Preferred)
            </a>
          </li>
          <li>
            <a
              href="https://store.steampowered.com/digitalgiftcards/selectgiftcard"
              target="_blank"
              class="flex items-center gap-2 hover:text-primary transition-colors font-bold"
            >
              <Icon icon="mdi:steam" /> Steam Wallet / Digital Gift Card
            </a>
          </li>
          <li>
            <a
              href="https://store.steampowered.com/wishlist/id/BittuX?sort=topsellers"
              target="_blank"
              class="flex items-center gap-2 hover:text-primary transition-colors font-bold"
            >
              <Icon icon="mdi:controller-classic" /> Gift a Wishlisted Game
            </a>
          </li>
        </ul>
        <p class="mt-5 font-light text-sm">You can also send other things besides gift cards — feel free to discuss it with me on Discord or email.</p>
      </section>
      <section
        class="bg-black/20 p-6 rounded-xl border border-white/5 flex flex-col md:flex-row justify-around items-center gap-6 text-center md:text-left"
      >
        <div class="flex flex-col gap-1">
          <p class="text-[10px] uppercase tracking-widest opacity-50">Steam Identity</p>
          <a
            href="https://steamcommunity.com/id/BittuX"
            class="flex items-center gap-2 text-sm text-primary hover:underline"
            target="_blank"
          >
            <Icon icon="mdi:steam" /> BittuX
          </a>
        </div>
        <div class="flex flex-col gap-1">
          <p class="text-[10px] uppercase tracking-widest opacity-50">
            Discord
          </p>
          <span class="flex items-center gap-2 text-sm text-primary">
            <Icon icon="mdi:discord" /> @bittu5134
          </span>
        </div>
        <div class="flex flex-col gap-1">
          <p class="text-[10px] uppercase tracking-widest opacity-50">Email</p>
          <a
            href="mailto:ssr7a5134@gmail.com"
            class="flex items-center gap-2 text-sm text-primary hover:underline"
          >
            <Icon icon="mdi:email" /> ssr7a5134@gmail.com
          </a>
        </div>
      </section>

      <section
        class="bg-base-200/50 p-6 rounded-xl border border-white/5 shadow-inner"
      >
        <div class="flex items-center gap-2 mb-4">
          <Icon icon="mdi:currency-btc" class="text-accent size-6" />
          <h2 class="text-xl font-semibold text-accent">Crypto Wallets</h2>
        </div>

        <div class="grid gap-4">
          {#each [{ label: "Bitcoin (BTC)", val: btc }, { label: "Ethereum (ETH)", val: eth }, { label: "Solana (SOL)", val: sol }] as coin}
            <div class="space-y-1">
              <p class="text-[10px] uppercase tracking-widest opacity-60 ml-1">
                {coin.label}
              </p>
              <button
                onclick={(e) => copy(coin.val, e)}
                class="w-full text-left font-mono text-[10px] md:text-xs p-4 bg-black/40 rounded-lg hover:bg-black/60 border border-white/5 hover:border-primary/50 transition-all break-all group"
              >
                {coin.val}
                <span
                  class="block text-[10px] text-primary mt-2 opacity-0 group-hover:opacity-100 transition-opacity"
                  >Click to copy address</span
                >
              </button>
            </div>
          {/each}
        </div>
      </section>
    </div>

    <footer class="mt-8 text-center relative z-10">
      <a
        href="/"
        class="btn btn-ghost btn-sm text-base-content/50 hover:text-primary transition-colors"
      >
        <Icon icon="mdi:arrow-left" /> Return to Home
      </a>
    </footer>
  </div>
</div>
