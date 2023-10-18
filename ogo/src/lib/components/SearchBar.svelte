<script>
    let searchTerm = '';
  
    function handleSearch() {
      // Implement your search logic here using the searchTerm variable
      console.log('Search term:', searchTerm);
    }
  </script>
  
  <div class="search-bar-container flex items-center border rounded p-2">
    <input type="text" class="flex-1 mr-2 outline-none" placeholder="Search for products..." bind:value={searchTerm} on:input={handleSearch} />
    <button class="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600">Search</button>
  </div>

  <style>
    .search-bar-container {
      width: 100%;
    }
  </style>