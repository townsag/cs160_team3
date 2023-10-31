<script>
  export let toggleFilterOpen;
  export let searchQuery;
  export let handleInput;
  export let startSearching;
</script>

<div class="search-bar-container flex items-center border rounded p-2">
  <input type="text" class="flex-1 mr-2 outline-none" placeholder="Search for products..." bind:value={searchQuery} on:input={handleInput} />
  <button class="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600" on:click={toggleFilterOpen}>Filter</button>
  <button class="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600" on:click={startSearching}>Search</button>
  <!-- 
    <button class="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600" on:click={() => handleSearch1(searchTerm)}>Search</button>
  -->
</div>

<style>
  .search-bar-container {
    width: 100%;
  }
</style>