<script>
  import Icon from "@iconify/svelte";
  import imgTheFool from "$lib/assets/web-the-fool.jpg?enhanced&w=9999";
</script>


<main
  class="flex min-h-dvh flex-col items-center justify-center gap-10 p-8 md:flex-row md:justify-around"
>
  <div class="hover-3d relative">
    <figure class="max-w-100 rounded-2xl shadow-2xl">
      <enhanced:img
        src={imgTheFool}
        alt="3D card"
        class="h-[75vh] max-h-[45vh] md:max-h-[75dvh] w-auto object-cover"
      />
    </figure>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
  </div>
  <div
    class="flex flex-col items-center md:items-start"
  >
    <div class="max-w-md text-center">
      <h1 class="lg:text-5xl text-3xl font-bold text-primary filter drop-shadow-[0_0_10px_#c47f0a] w-full block md:text-left">
        Lord of the Mysteries
      </h1>
      <p class="py-6 lg:text-2xl text-lg lg:w-full md:w-4/5 w-full brightness-95 md:text-left">
        “The Fool that doesn’t belong to this era, <br>
        the mysterious ruler above the gray fog; <br>
        the King of Yellow and Black who wields good luck…”
      </p>
    </div>

    <div class="flex gap-4">
      <a class="btn btn-lg btn-soft btn-primary" href="/book">Read Now</a>
      <a class="btn btn-lg btn-soft btn-secondary" href="/download">Download</a>
    </div>
  </div>

  <div class="fixed right-0 lg:top-1/3 top-2/9 z-50 flex flex-col gap-2 pr-2">
    <div class="tooltip tooltip-left" data-tip="Donate">
      <a href="/donate" class="btn btn-soft btn-lg btn-secondary"
        ><Icon icon="mdi:heart-outline" class="size-7" /></a
      >
    </div>
    <div class="tooltip tooltip-left" data-tip="Info">
      <a
        href="https://github.com/Bittu5134/LOTM-Reader"
        class="btn btn-soft btn-lg btn-info"
        ><Icon icon="mdi:information-outline" class="size-7" /></a
      >
    </div>
    <div class="tooltip tooltip-left" data-tip="Contribute">
      <a
        href="https://github.com/Bittu5134/ORV-Reader/blob/main/contributing.md"
        class="btn btn-soft btn-lg btn-warning"
        ><Icon icon="ri:edit-line" class="size-7" /></a
      >
    </div>
    <div class="tooltip tooltip-left" data-tip="Discord">
      <a
        href="https://discord.gg/XmzJVsyuTQ"
        class="btn btn-soft btn-lg btn-accent"
        ><Icon icon="mingcute:discord-line" class="size-7" /></a
      >
    </div>
  </div>
</main>
