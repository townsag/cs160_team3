

<script lang="ts">
	//import logo from "../assets/logo.png";
  import SearchBar from '../lib/components/SearchBar.svelte';
  import FilterBar from '../lib/components/FilterBar.svelte';
  import ItemDisplay from '../lib/components/ItemDisplay.svelte';
  //mport Data from '../../../app.py';

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
  /*
  let items = [
    {
      id: 1,
      name: 'Apple',
      category: 'Fruits',
      price: 19.99,
      weight: '5.51 lbs',
      photoUrl: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTN2Hgg8YOw4ntI9XZl0XX4ppf2VmSYyMrwJjFJhpYJrMeMt6y0XcMqdrQwUytsYfMldkI&usqp=CAU',
      tags: ['Gluten Free', 'Vegetarian', 'Vegan']
    },
    {
      id: 2,
      name: 'Eggplant',
      category: 'Fruits',
      price: 29.99,
      weight: '3.31 lbs',
      photoUrl: 'https://mucci-production-user-uploads-bucket.s3.amazonaws.com/images/Product-IMG_MiniEggplant-rev.original.png',
      tags: ['Vegetarian']
    },
    // Add more items as needed
    {
      id: 3,
      name: 'Banana',
      category: 'Fruits',
      price: 9.99,
      weight: '7.72 lbs',
      photoUrl: 'https://th-thumbnailer.cdn-si-edu.com/4Nq8HbTKgX6djk07DqHqRsRuFq0=/1000x750/filters:no_upscale()/https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/d5/24/d5243019-e0fc-4b3c-8cdb-48e22f38bff2/istock-183380744.jpg',
      tags: []
    },
    {
      id: 4,
      name: 'Beef',
      category: 'Protein',
      price: 4.99,
      weight: '5.51 lbs',
      photoUrl: 'https://images.inc.com/uploaded_files/image/1920x1080/getty_80116649_344560.jpg',
      tags: []
    },
    {
      id: 5,
      name: 'Cheese',
      category: 'Protein',
      price: 6.99,
      weight: '9.92 lbs',
      photoUrl: 'https://cdn.britannica.com/60/217660-050-DBCC409A/cheddar-cheese-wedge.jpg',
      tags: []
    },
    {
      id: 6,
      name: 'Chicken',
      category: 'Protein',
      price: 14.99,
      weight: '2.65 lbs',
      photoUrl: 'https://images.eatthismuch.com/img/395_ldementhon_471464da-daad-4a92-8b5d-7e9a6de898a8.png',
      tags: []
    },
    {
      id: 7,
      name: 'Almonds',
      category: 'Nuts',
      price: 23.99,
      weight: '6.17 lbs',
      photoUrl: 'https://www.healthysupplies.co.uk/pics/almonds-catpic21.jpg',
      tags: ['Vegan']
    },
    {
      id: 8,
      name: 'Walnuts',
      category: 'Nuts',
      price: 39.99,
      weight: '1.98 lbs',
      photoUrl: 'https://cdn.britannica.com/69/124169-050-54860BD1/fruit-walnut-tree-husk.jpg',
      tags: []
    }
    // Add more items with tags
  ]; */

  import { onMount } from 'svelte';

  let items = {}; // Initialize items as an empty array

  async function getItemsList() {
    const response = await fetch('/getProducts');
    const data = await response.json();
    // return {
    //   props: {
    //     items: data, // Assuming the response contains the items array
    //   },
    // };
    return JSON.stringify(data);
  }

  items = getItemsList();
  console.log(items);

  // onMount(() => {
  //   console.log("mounted");
  //   items = getItemsList();
  //   console.log(items);
  // });

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

<style>
  .blur {
    filter: blur(5px); /* You can adjust the blur intensity as needed */
  }
</style>

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