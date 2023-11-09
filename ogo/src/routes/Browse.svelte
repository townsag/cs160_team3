

<script lang="ts">
	import SearchBar from '../lib/components/SearchBar.svelte';
  import FilterBar from '../lib/components/FilterBar.svelte';
  import ItemDisplay from '../lib/components/ItemDisplay.svelte';

  let currentCategory = "";
  let filterTags: any[] = [];

  let currentUser;
  let isAdmin = false;

  let isCartItem = false;

  let API_KEY: string = "none";

  function toggleCategory(currCategory: string) {
    currentCategory = currCategory;
    //console.log(currentCategory);
  }
  function toggleTags(toggleTagsList: any[]) {
    filterTags = [];
    for (let i = 0; i < toggleTagsList.length; i++) {
      if (toggleTagsList[i] == true) {
        filterTags.push(allTagsList[i].name);
      }
    }
    //console.log(toggleTagsList);
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
  function handleInput(event: any) {
    searchQuery = event.target.value;
  }

  import { onMount } from 'svelte';

  let items: any[] = [];
  let searchBarItems: any[] = [];
  let filteredItems: any[] = [];

  let allTagsList: any[] = [];
  let allCategoriesList: any[] = [];

  async function sequential_api_calls(){
    const route_id = 1;
    try{                                  //getAllItems
      const response = await fetch("/getProducts", { method: "GET" });
      const data = await response.json();
      items = data;
      console.log("All Items: " + data);
    } catch (error) {
        console.log("error: ", error);
    }
    try{                                  //updateSearchBarFilter
      const response = await fetch("/searchProducts?" + new URLSearchParams({ query: searchQuery })) 
      const data = await response.json();
      searchBarItems = data;
      console.log("SearchBar: " + data);
    } catch (error) {
        console.log("error: ", error);
    }
    try{                                  //getAllTags
      const response = await fetch("/getTags", { method: "GET" });
      const data = await response.json();
      allTagsList = data;
      console.log("allTagsList: " + data);
    } catch (error) {
        console.log("error: ", error);
    }
    try{                                  //getAllCategories
      const response = await fetch("/getCategories", { method: "GET" });
      const data = await response.json();
      allCategoriesList = data;
      console.log("allCategoriesList: " + data);
    } catch (error) {
        console.log("error: ", error);
    }
    try{                                  //getUser
      const response = await fetch("/getUser", { method: "GET" });
      const data = await response.json();
      currentUser = data;
      isAdmin = currentUser.is_admin;
      //console.log("isAdmin: " + isAdmin);
    } catch (error) {
        console.log("error: ", error);
    }
  }

  async function updateSearchBarFilter() {
    try{                                  //updateSearchBarFilter
      const response = await fetch("/searchProducts?" + new URLSearchParams({ query: searchQuery })) 
      const data = await response.json();
      searchBarItems = data;
    } catch (error) {
        console.log("error: ", error);
    } 
  }

  function findMatch(item: any) {
    for (let i = 0; i < searchBarItems.length; i++) {
      if (searchBarItems[i].name == item.name)
        return true;
    }
    return false;
  }

  onMount(async () => {
    sequential_api_calls();
  });

  $: {
    if (startSearch == true) {
      updateSearchBarFilter();
      startSearch = false;
      //console.log("query: " + searchQuery);
      console.log("query list: " + searchBarItems);
    } 

    filteredItems = items.filter((item) => {
      if (!findMatch(item)) {
        return false;
      } 
      
      if (currentCategory != "" && currentCategory != item.category.name) {
        return false;
      } 

      let tempTags = [];
      for (let i = 0; i < item.tags.length ; i++) {
        let tempName = item.tags[i].name;
        tempTags.push(tempName);
      }
      for (let i = 0; i < filterTags.length; i++) {
        if (!tempTags.includes(filterTags[i])) {
          return false;
        }
      }

      return true; 
    }); 

    let tempNameList = []
    for (let i = 0; i < filteredItems.length; i ++) {
      tempNameList.push(filteredItems[i].name);
    }
    console.log("displayed list (names): " + tempNameList);
  } 
</script>

<style>
  .blur {
    filter: blur(5px); /* You can adjust the blur intensity as needed */
  }
</style>

<div class="container mx-auto p-4">
  <div class="search-bar-container flex items-center border rounded ,," >
    <SearchBar 
      {toggleFilterOpen}
      {searchQuery}
      {handleInput}
      {startSearching}
    />
  </div>

  <div class="{openFilter ? '' : 'blur'}">
    <ItemDisplay 
      {filteredItems}
      {isAdmin}
      {isCartItem}
    />
  </div>

  <div class="flex">
    <div class="w-4/4 pr-4">
      <div>
        <FilterBar
          {openFilter}
          {toggleFilterOpen}
          {allCategoriesList}
          {allTagsList}
          {toggleCategory}
          {toggleTags}
        />
      </div>
    </div>
  </div>
</div>

