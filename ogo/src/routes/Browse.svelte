

<script lang="ts">
	import SearchBar from '../lib/components/SearchBar.svelte';
  import ItemDisplay from '../lib/components/ItemDisplay.svelte';
  import Navbar from "../lib/components/Navbar.svelte";

  import { alert } from '../lib/stores/alertStore';
  import AlertDaisy from "../lib/components/AlertDaisy.svelte";

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
  let openFilter = false;
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

  let noClick: any;
  let noScroll: any;
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


    noClick = openFilter ? 'pointer-events-none' : '';
    noScroll = openFilter ? 'overflow-hidden' : 'overflow-show';
    if (openFilter) {
      document.body.classList.add('overflow-hidden');
    } else {
      document.body.classList.remove('overflow-hidden');
    }
  } 

  function handleCategoryChange(event: any) {
    // Retrieve the selected category value from the event
    const selectedCategory = event.target.value;

    // Call your function with the selected category value
    toggleCategory(selectedCategory);
  }

  let toggleTagsList = new Array(allTagsList.length);
  function toggleTag(tagName: string) {
    for (let i = 0; i < allTagsList.length; i++) {
      if (allTagsList[i].name == tagName) {
        toggleTagsList[i] = !toggleTagsList[i];
      }
    } 
    toggleTags(toggleTagsList);
  }
</script>

<style>
  .blur {
    filter: blur(5px); /* You can adjust the blur intensity as needed */
  }

  .pointer-events-none {
    pointer-events: none;
  }

  .overflow-show {
    overflow: scroll;
  }

  .overflow-hidden {
    overflow: hidden;
  }

  .filter-content {
    padding: 20px;
    width: 350px;
  }

  .filter-item {
    margin-bottom: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .filter-item label {
    margin-right: 10px; /* Add margin between label and checkbox */
  }

  .filter-test {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0; /* Set bottom to 0 to make it touch the bottom */
    width: 370px;
    overflow-y: auto;
    box-shadow: 5px 0 10px rgba(0, 0, 0, 0.5);
  }
</style>

<Navbar/>
<AlertDaisy {alert} />
<div class="container mx-auto p-4">
  <div class="{openFilter ? 'blur' : ''} {noClick}">
    <SearchBar 
      {toggleFilterOpen}
      {searchQuery}
      {handleInput}
      {startSearching}
    />
  </div>

  <div class="{openFilter ? 'blur' : ''} {noClick}">
    <ItemDisplay 
      {filteredItems}
      {isAdmin}
      {isCartItem}
    />
  </div>

  <div class="drawer">
    <input id="my-drawer" type="checkbox" class="drawer-toggle" bind:checked={openFilter}/>
    <div class="drawer-side">
      <label for="my-drawer" aria-label="close sidebar" class="drawer-overlay"></label>
      <ul class="menu filter-test p-2 min-h-full bg-base-200 text-base-content">
        <div class="filter-content">
          <div class="filter-item">
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label class="text-lg font-normal">Category: </label>
            <select class="select text-lg font-normal" on:change={handleCategoryChange}>
              <option value="">All</option>
              {#each allCategoriesList as category}
                <option value={category.name}>{category.name}</option>
              {/each}
            </select>
          </div>
          {#each allTagsList as tag}
              <div class="form-control">
                <label class="label cursor-pointer text-lg font-normal" style="padding: 2px;">
                  <span class="label-text text-lg font-normal">{tag.name}</span> 
                  <input type="checkbox" class="checkbox checkbox-primary" on:change={() => toggleTag(tag.name)}/>
                </label>
              </div>
          {/each}
        </div>
      </ul>
    </div>
  </div>
</div>
