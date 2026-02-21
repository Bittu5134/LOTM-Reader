<script>
// [IMG_IMPORT]
import css from "../../../../reader.css?url"
import { readerState } from "$lib/reader.svelte.ts";
// [METADATA]
readerState.ch_meta = ch_meta;
</script>

<svelte:head>
  <link rel="stylesheet" href={css} />
</svelte:head>

<style>

  /* img {
    border-radius: 0.5em;
    max-height: 85vh;
    width: auto;
    margin: auto;
  }

  figcaption {
    font-size: medium;
    margin-top: 0.5em;
    text-align: center;
  }
  img.hidden-caption + figcaption {
    display: none;
  }
  .hidden-caption + figcaption {
    display: none;
  }
  figure:has(.hidden-caption) figcaption {
  display: none;
}
  h1,
  h2,
  h3 {
    text-align: center;
    position: relative;
    padding-bottom: 0.5em;
    margin-bottom: 1.5em;
    font-variant: small-caps;
  }

  h1::after,
  h2::after,
  h3::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 30%; 
    height: 3px;
    background-color: currentColor; 
    border-radius: 2px;
  } */
</style>

<!-- [DATA] -->