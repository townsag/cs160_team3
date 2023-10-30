<script>
  //array size not updating
  export let filteredItems;
  
  //let displayedItem = [];
  //displayedItem = filteredItems;
  //console.log("displayed list (in itemdisplay): " + displayedItem);
</script>

<style>
  .grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); /* Use minmax for flexible column sizing */
    gap: 20px; /* Adjust the gap between items */
    justify-content: center; /* Center items within the grid */
    grid-auto-rows: minmax(150px, auto); /* Set a minimum and maximum row height */
    min-height: 80vh;
  }

  .border {
    min-width: 150px;
    min-height: 150px;
    padding: 10px;
  }
</style>

<div class="grid-container mt-4">
  {#each filteredItems as item}
    <div class="border p-4 rounded-lg shadow-md hover:shadow-xl transition duration-300">
      <img src={item.image} alt={item.name} class="mb-2 w-full h-40 object-cover" />

      <div class="flex flex-col">
        <div class="mb-2">
          <h2 class="text-lg font-semibold">{item.name}</h2>
          <p class="text-gray-600 mb-1">{item.category.name}</p>
          <p class="text-green-600 font-semibold">${item.price.toFixed(2)}</p>
          <p class="text-gray-600">{item.weight} lbs</p>
        </div>

        <!-- Tags (only display if tags exist) -->
        {#if item.tags && item.tags.length > 0}
          <div class="flex flex-wrap">
            {#each item.tags as tag (tag)}
              <span class="bg-gray-200 text-gray-800 px-2 py-1 rounded-full text-sm mr-2 mb-2">{tag.name}</span>
            {/each}
          </div>
        {/if}
      </div>
    </div>
  {/each}
</div>