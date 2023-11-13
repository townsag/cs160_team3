<script lang='ts'>
  export let toggleFilterOpen: any;
  export let searchQuery: string;
  export let handleInput: any;
  export let startSearching: any;

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      startSearching();
    }
  };
</script>

<div class="search-bar-container flex items-center border rounded-lg p-2 shadow-md">
  <input type="text" class="flex-1 mr-2 pl-2 outline-none text-lg font-normal" placeholder="Search for products..." bind:value={searchQuery} on:input={handleInput} on:keydown={handleKeyDown}/>
  <button class="bg-white text-white px-3 py-1 rounded" on:click={toggleFilterOpen}>
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
      <path d="M1 0h22l-9 15.094v8.906l-4-3v-5.906z"/>
    </svg>
  </button>
  <button class="btn bg-secondary text-white rounded-lg" on:click={startSearching}>
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M21.172 24l-7.387-7.387c-1.388.874-3.024 1.387-4.785 1.387-4.971 0-9-4.029-9-9s4.029-9 9-9 9 4.029 9 9c0 1.761-.514 3.398-1.387 4.785l7.387 7.387-2.828 2.828zm-12.172-8c3.859 0 7-3.14 7-7s-3.141-7-7-7-7 3.14-7 7 3.141 7 7 7z"/></svg>
  </button>
</div>

<style>
  .search-bar-container {
    width: 100%;
  }
</style>