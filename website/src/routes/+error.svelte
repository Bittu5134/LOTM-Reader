<script>
  import favicon from "$lib/assets/favicon.svg";
  import imgBG from "$lib/assets/web-bg.jpg?enhanced&w=9999";
  import "../app.css";
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<div class="fixed inset-0 -z-10 overflow-hidden">
  <enhanced:img 
    src={imgBG} 
    alt="" 
    class="w-full h-full object-cover" 
  />
  
  <div class="absolute inset-0 bg-black/50 backdrop-blur-xs"></div>
</div>

<main
  class="relative flex min-h-dvh flex-col items-center justify-center overflow-hidden px-6 text-center"
>
  <div class="max-w-md space-y-6">
    <h2
      class="font-serif text-3xl font-bold tracking-tight text-base-content md:text-5xl"
    >
      [404] Lost in the Grey Fog
    </h2>

    <p class="text-lg leading-relaxed text-base-content/70 italic">
      "The path you seek is veiled by secrets. Even a Beyonder of high sequence
      cannot find what does not exist in this era."
    </p>

    <div class="flex flex-col justify-center gap-4 sm:flex-row">
      <a href="/" class="btn btn-primary btn-lg shadow-lg">
        Return to the Fog
      </a>
      <button
        onclick={() => window.history.back()}
        class="btn btn-outline btn-lg"
      >
        Go Back
      </button>
    </div>
  </div>
</main>
