<script>
  export let openFilter;
  export let toggleFilterOpen;
  export let toggleGlutenFree;
  export let toggleVegetarian;
  export let toggleVegan;
  export let allCategoriesList;
  export let allTagsList;
  export let toggleCategory;
  export let toggleTags;

  //overflow-y: scroll;

  function handleCategoryChange(event) {
    // Retrieve the selected category value from the event
    const selectedCategory = event.target.value;

    // Call your function with the selected category value
    toggleCategory(selectedCategory);
  }

  let toggleTagsList = new Array(allTagsList.lenght);
  function toggleTag(tagName) {
    for (let i = 0; i < allTagsList.length; i++) {
      if (allTagsList[i].name == tagName) {
        toggleTagsList[i] = !toggleTagsList[i];
      }
    } 
    toggleTags(toggleTagsList);
  }
</script>

<style>
  .filter-bar-container {
    position: absolute;
    top: 106px;
    left: 0;
    bottom: 0; /* Set bottom to 0 to make it touch the bottom */
    width: 300px;
    background-color: #f5f5f5;
    box-shadow: 0px 0px 5px 0px rgba(0, 0, 0, 0.2);
    transition: width 0.3s ease-out;
    overflow-y: auto;
  }

  .filter-bar-container.collapsed {
    width: 0px;
  }

  .filter-content {
    padding: 20px;
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
    width: 50px;
    height: 100%;
    background-color: #333;
    color: white;
    border: none;
    cursor: pointer;
  }

  .smoll-button {
    position: absolute;
    top: 0;
    right: 0;
    width: 20px;
    height: width;
    background-color: #f5f5f5;
    border: none;
    cursor: pointer;
  }
</style>

<div class="filter-bar-container" class:collapsed={openFilter}>
  <div class="filter-content">
    <div class="filter-item">
      <label>Category: </label>
      <select on:change={handleCategoryChange}>
        <option value="">All</option>
        {#each allCategoriesList as category}
          <option value={category.name}>{category.name}</option>
        {/each}
      </select>
    </div>
    {#each allTagsList as tag}
      <div class="filter-item">
        <label>{tag.name}:</label>
        <input type="checkbox" on:change={() => toggleTag(tag.name)} />
      </div>
    {/each}
  </div>
  <button class="smoll-button" on:click={toggleFilterOpen}>{'X'}</button>
</div>