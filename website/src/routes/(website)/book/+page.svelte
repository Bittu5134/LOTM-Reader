<script>
  import imgLOTM from "$lib/assets/web-lotm-cover.jpg?enhanced&w=9999";
  import imgCOI from "$lib/assets/web-coi-cover.jpg?enhanced&w=9999";
</script>



<main
  class="min-h-dvh flex flex-col items-center justify-center gap-10 p-8 md:flex-row md:justify-evenly"
>
  <a class="hover-3d static" href="./lotm">
    <figure class="md:w-80 w-60 rounded-2xl cursor-pointer">
      <enhanced:img
        src={imgLOTM}
        alt="Lord of the Mysteries Book Cover"
      />
    </figure>
    <!-- 8 empty divs needed for the 3D effect -->
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
  </a>

  <a class="hover-3d relative cursor-pointer" href="./coi">
    <!-- content -->
    <figure class="md:w-80 w-60 rounded-2xl">
      <enhanced:img
        src={imgCOI}
        alt="Conspiracy of the Infinite Book Cover"
      />
    </figure>
    <!-- 8 empty divs needed for the 3D effect -->
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
  </a>
</main>
