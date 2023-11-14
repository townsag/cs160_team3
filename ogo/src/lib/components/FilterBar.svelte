<script lang='ts'>
  export let openFilter: Boolean;
  export let toggleFilterOpen: any;
  export let allCategoriesList: any[];
  export let allTagsList: any[];
  export let toggleCategory: any;
  export let toggleTags: any;

  //overflow-y: scroll;

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

  let notOpen = !openFilter;
  $: {
    notOpen = !openFilter;
  }
</script>

<style>
  .filter-bar-container {
    position: absolute;
    top: 67px;
    left: 0;
    bottom: 0; /* Set bottom to 0 to make it touch the bottom */
    width: 350px;
    background-color: white;
    box-shadow: 0px 0px 5px 0px rgba(0, 0, 0, 0.2);
    transition: width 0.3s ease-out;
    overflow-y: auto;
  }

  .filter-bar-container.collapsed {
    width: 0px;
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
  
  .collapse-button {
    position: absolute;
    top: 0;
    right: 0;
    width: 35px;
    height: 100%;
    color: black;
    border: none;
    cursor: pointer;
  }

  .smoll-button {
    position: absolute;
    top: 0;
    right: 0;
    width: 20px;
    height: width;
    background-color: white;
    border: none;
    cursor: pointer;
  }

  .filter-test {
    position: fixed;
    top: 67px;
    left: 0;
    bottom: 0; /* Set bottom to 0 to make it touch the bottom */
    width: 390px;
    overflow-y: auto;
    box-shadow: 5px 0 10px rgba(0, 0, 0, 0.2);
  }
</style>

<div class="drawer">
  <input id="my-drawer" type="checkbox" class="drawer-toggle" bind:checked={notOpen}/>
  <div class="drawer-side">
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
      <button class="collapse-button bg-secondary text-lg" on:click={toggleFilterOpen}>{'<'}</button>
    </ul>
  </div>
</div>