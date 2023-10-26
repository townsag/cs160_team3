

<script lang="ts">
	import SearchBar from '../lib/components/SearchBar.svelte';
  import FilterBar from '../lib/components/FilterBar.svelte';
  import ItemDisplay from '../lib/components/ItemDisplay.svelte';

  let isGlutenFree = false;
  let isVegetarian = false;
  let isVegan = false; 
  function toggleGlutenFree() {
    isGlutenFree = !isGlutenFree;
  }
  function toggleVegetarian() {
    isVegetarian = !isVegetarian;
  }
  function toggleVegan() {
    isVegan = !isVegan;
  }

  //search bar stuff
  let openFilter = true;
  let searchQuery = '';
  let startSearch = false;
  function toggleFilterOpen() {
    openFilter = !openFilter;
  }
  function startSearching() {
    startSearch = true;
  }
  function handleInput(event) {
    searchQuery = event.target.value;
  }

  import { onMount } from 'svelte';

  let items: any[] = [];
  let searchBarItems: any[] = [];
  let filteredItems = [];

  // Use onMount to fetch data when the component is mounted
  onMount(async () => {
    const response = await fetch("/getProducts", { method: "GET" });
    const data = await response.json();
    items = data;
    updateSearchBarFilter();
    //getAllTags();
  });

  async function updateSearchBarFilter() {
    //const response = await fetch("/searchProducts", { method: "GET" });
    const response = await fetch("/searchProducts?" + new URLSearchParams({ query: searchQuery })) 
    //const response = await fetch("/searchProducts?query=" + searchQuery);
    const data = await response.json();
    searchBarItems = data;
  }

  let allTags = [];
  async function getAllTags() {
    const response = await fetch("/getTags", { method: "GET" });
    const data = await response.json();
    allTags = data;
    console.log(allTags);
  }

  function findMatch(item) {
    for (let i = 0; i < searchBarItems.length; i++) {
      if (searchBarItems[i].name == item.name)
        return true;
    }
    return false;
   }

  // revert back to old but make it so that if query != '' then filter items will have toi b like if item is in searchbarItems befor checking tags?
  $: {
    
    if (startSearch == true) {
      updateSearchBarFilter();
      startSearch = false;
      console.log("query: " + searchQuery);
      console.log("actual list: " + searchBarItems);
    } 

    filteredItems = items.filter((item) => {
      //if (searchQuery != '' && !searchBarItems.includes(item)) {
      if (!findMatch(item)) {
        return false;
      } 
      let tempTags = [];
      for (let i = 0; i < item.tags.length ; i++) {
        let tempName = item.tags[i].name;
        tempTags.push(tempName);
      }
      if (isGlutenFree && !tempTags.includes('Gluten Free')) {
        return false;
      }
      if (isVegetarian && !tempTags.includes('Vegetarian')) {
        return false;
      }
      if (isVegan && !tempTags.includes('Vegan')) {
        return false;
      }
      return true;
    }); 

    //filteredItems = searchBarItems;


    let tempNameList = []
    for (let i = 0; i < filteredItems.length; i ++) {
      tempNameList.push(filteredItems[i].name);
    }
    console.log("displayed list: " + filteredItems);
    console.log("displayed list (names): " + tempNameList);
  } 
</script>

<div class="container mx-auto p-4">
  <div class="flex">
    <div class="w-4/4 pr-4">
      <FilterBar
        {openFilter}
        {toggleGlutenFree}
        {toggleVegetarian}
        {toggleVegan}
      />
    </div>
  </div>

  <div class="search-bar-container flex items-center border rounded p-2 mb-4" >
    <SearchBar 
      {toggleFilterOpen}
      {searchQuery}
      {handleInput}
      {startSearching}
    />
  </div>

  <div>
    <ItemDisplay 
      {filteredItems}
    />
  </div>
</div>