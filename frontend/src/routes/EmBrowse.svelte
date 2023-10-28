

<script lang="ts">
  import SearchBar from '../lib/components/SearchBar.svelte';
  import FilterBar from '../lib/components/FilterBar.svelte';
  import ItemDisplay from '../lib/components/ItemDisplay.svelte';

  let openFilter = true;

  let isGlutenFree = false;
  let isVegetarian = false;
  let isVegan = false; 

  function toggleFilterOpen() {
    openFilter = !openFilter;
  }

  function toggleGlutenFree() {
    isGlutenFree = !isGlutenFree;
  }

  function toggleVegetarian() {
    isVegetarian = !isVegetarian;
  }

  function toggleVegan() {
    isVegan = !isVegan;
  }

  let items = {}; // Initialize items as an empty array

  async function getItemsList() {
    const response = await fetch('/getProducts');
    const data = await response.json();
    return JSON.stringify(data);
  }

  items = getItemsList();
  console.log(items);

  let filteredItems = [];

  $: {
    filteredItems = items.filter((item) => {
      if (isGlutenFree && !item.tags.includes('Gluten Free')) {
        return false;
      }

      if (isVegetarian && !item.tags.includes('Vegetarian')) {
        return false;
      }

      if (isVegan && !item.tags.includes('Vegan')) {
        return false;
      }

      return true;
    });
  }
</script>

<div class="container mx-auto p-4">
  <div class="flex">
    <div class="w-4/4 pr-4">
      <FilterBar
        {openFilter}
        {isGlutenFree}
        {isVegetarian}
        {isVegan}
        {toggleGlutenFree}
        {toggleVegetarian}
        {toggleVegan}
      />
    </div>
  </div>

  <div class="search-bar-container flex items-center border rounded p-2 mb-4" >
    <SearchBar 
      {openFilter}
      {toggleFilterOpen}
    />
  </div>

  <div>
    <ItemDisplay 
      {items} 
      {filteredItems} 
    />
  </div>
</div>