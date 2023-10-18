<script>
  let isCollapsed = true;
  export let isGlutenFree;
  export let isVegetarian;
  export let isVegan;
  export let toggleGlutenFree;
  export let toggleVegetarian;
  export let toggleVegan;

  function toggleCollapse() {
    isCollapsed = !isCollapsed;
  }
  
</script>

<style>
  .filter-bar-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 300px;
    height: 100%;
    background-color: #f5f5f5;
    box-shadow: 0px 0px 5px 0px rgba(0, 0, 0, 0.2);
    transition: width 0.3s ease-out;
    overflow-y: auto;
  }

  .filter-bar-container.collapsed {
    width: 50px;
  }

  .filter-content {
    padding: 20px;
  }

  .filter-item {
    margin-bottom: 15px;
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
</style>

<div class="filter-bar-container" class:collapsed={isCollapsed}>
  <div class="filter-content">
    <div class="filter-item">
      <label>Toggle Filter:</label>
      <input type="checkbox" />
    </div>

    <div class="filter-item">
      <label>Dropdown Filter:</label>
      <select>
        <option value="">Option 1</option>
        <option value="">Option 2</option>
      </select>
    </div>

    <div class="filter-item">
      <label>Input Filter:</label>
      <input type="text" placeholder="Enter value" />
    </div>

    <div class="filter-item">
      <label>Gluten Free:</label>
      <input type="checkbox" on:change={toggleGlutenFree} />
    </div>
  
    <div class="filter-item">
      <label>Vegetarian:</label>
      <input type="checkbox" on:change={toggleVegetarian} />
    </div>
  
    <div class="filter-item">
      <label>Vegan:</label>
      <input type="checkbox" on:change={toggleVegan} />
    </div>
  </div>
  <button class="collapse-button" on:click={toggleCollapse}>
    {isCollapsed ? 'Show Filters' : 'Hide Filters'}
  </button>
</div>