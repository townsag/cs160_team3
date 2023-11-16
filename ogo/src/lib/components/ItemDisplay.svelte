<script lang='ts'>
  //array size not updating
  import { navigate } from "svelte-routing";
  import { removeCartItem, updateCartItem, getProductById } from "../util/RequestController"
  import { cartItemQuantitySignal, cartItemRemovedSignal } from "../stores/CartObserver";

  import { alert } from '../stores/alertStore';
  import AlertDaisy from "./AlertDaisy.svelte";

  export let filteredItems: any[];
  export let isAdmin: Boolean;
  export let isCartItem: Boolean;

  function handleItemClick(item: any) {
    if (!isCartItem) {
      //navigate(`/itemView/${item.product_id}`, { state: { item } });
      navigate(`/itemView/${item.product_id}`);

      console.log("ItemDisplay: " + item.name);
    }
  }

  function handleCreateItemClick() {
    if (!isCartItem) {
      navigate(`/itemView/${0}`);

      console.log("Clicked on create item");
    }
  }

  //
  // BELOW USED IF ITEM DISPLAY IS FOR CART ITEM
  //

  // Cart Item Removal
  async function handleRemoveCartItem(item: any) {
    const result = await removeCartItem(item.cart_item_id);

    if (result.success) {
        console.log("Cart item removed successfully.");
        alert.set({ show: true, message: 'Cart item removed successfully', type: 'success'});
        cartItemRemovedSignal.set(!$cartItemRemovedSignal);
    } else {
        console.error("Failed to remove cart item:", result.message);
        alert.set({ show: true, message: 'Failed to remove cart item: ' + result.message, type: 'error'});
    }
  }

  // Cart Item Quantity Change
  async function handleQuantityChange(item: any, event: any) {
    try {
      const product = await getProductById(item.product_id);
      const productStock = product.quantity;
      
      let newCartItemQuantity = parseInt(event.target.value, 10);

      // quantity = not-a-number check
      if (isNaN(newCartItemQuantity)) {
        console.log("Inputted quantity is not a number, possibly whitespace.");
        //alert.set({ show: true, message: 'Quantity must be a number', type: 'error'});
        return;
      }

      // quantity <= zero quantity check
      if (newCartItemQuantity <= 0) {
        event.target.value = 1;
        console.log("Inputted quantity cannot be zero.");
        alert.set({ show: true, message: 'Unexpected zero quantity count', type: 'error'});
        return;
      }

      // quantity > stock check, if over then reset to max stock and proceed
      if (newCartItemQuantity > productStock) {
        event.target.value = productStock;
        newCartItemQuantity = productStock;
        console.log("Inputted quantity is over the stock in inventory.");
        alert.set({ show: true, message: `There is only ${productStock} of this item left in stock`, type: 'error'});
      }

      // if cart item quantity is greater than 0
      if (newCartItemQuantity > 0) {
        try {
          const result = await updateCartItem(item.cart_item_id, item.product_id, newCartItemQuantity);

          if (result.success) {
            console.log(item.cart_item_id, item.category.name, "Cart item updated successfully: Quantity changed.");
            cartItemQuantitySignal.set(!$cartItemQuantitySignal);
            //alert.set({ show: true, message: 'Quantity changed successfully', type: 'success'});
          } else {
            console.error("Failed to update cart item:", result.message);
            alert.set({ show: true, message: 'Failed to update cart item: ' + result.message, type: 'error'});
            location.reload();
          }
        } catch (error) {
          console.log("An error occurred:", error)
          alert.set({ show: true, message: 'An error occurred: ' + error, type: 'error'});
        }
      } else {
        console.log("Inputted quantity would make the cart over the weight limit.");
        alert.set({ show: true, message: 'Total weight is over the weight limit', type: 'error'});
      }
    } catch (error) {
      console.log("An error occurred:", error);
      alert.set({ show: true, message: 'An error occurred: ' + error, type: 'error'});
    }
  }

  // filters non-numbers such as "e" and "."
  function onlyNumbers(event: any) {
    const charCode = event.which ? event.which : event.keyCode;

    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
      event.preventDefault();
    }
  }
</script>

<style>
  .grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); /* Use minmax for flexible column sizing */
    gap: 20px; /* Adjust the gap between items */
    justify-content: center; /* Center items within the grid */
  }

  .border {
    min-width: 150px;
    min-height: 150px;
    max-height: 500px;
    padding: 10px;
  }

  body {
    margin: 0;
    padding: 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .disable-spin-buttons::-webkit-inner-spin-button,
  .disable-spin-buttons::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
</style>

<body>
  <AlertDaisy {alert} />
  <div class="grid-container">
    {#if isAdmin && !isCartItem}
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-static-element-interactions -->
      <div on:click={() => handleCreateItemClick()} class="border p-4 rounded-lg shadow-md hover:shadow-xl transition duration-300">
        <img src={"https://cdn.vectorstock.com/i/preview-1x/98/76/plus-sign-vector-46979876.jpg"} alt={"Plus Sign"} class="mb-2 w-full h-60 object-cover" />
        <div class="flex flex-col">
          <div class="mb-2">
            <h2 class="text-lg font-semibold">{"ADD PRODUCT"}</h2>
          </div>
        </div>
      </div>
    {/if}

    {#each filteredItems as item}
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <!-- svelte-ignore a11y-no-static-element-interactions -->
      <div on:click={() => handleItemClick(item)} class="grid grid-rows-[auto,1fr] border p-4 rounded-lg shadow-md hover:shadow-xl transition duration-300">
        <img src={item.image} alt={item.name} class="mb-2 w-full h-40 object-cover" />
  
        <div class="flex flex-col">
          <div class="mb-2">
            <h2 class="text-lg font-semibold">{item.name}</h2>
            <p class="text-gray-600 mb-1">{item.category.name}</p>
            <p class="text-green-600 font-semibold">${item.price.toFixed(2)}</p>
            <p class="text-gray-600">{item.weight} lb.</p>
          </div>
  
          <!-- Tags (only display if tags exist) -->
          {#if item.tags && item.tags.length > 0}
            <div class="flex flex-grow flex-wrap items-start overflow-y-auto">
              {#each item.tags as tag (tag)}
                <span class="bg-gray-200 text-gray-800 px-2 py-1 rounded-full text-xs mr-1 mb-2">
                  {tag.name}
                </span>
              {/each}
            </div>
          {/if}
        </div>

        {#if isCartItem}
          <div class="flex flex-col">
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <div class="flex flex-row items-center justify-between">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bag-plus" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M8 7.5a.5.5 0 0 1 .5.5v1.5H10a.5.5 0 0 1 0 1H8.5V12a.5.5 0 0 1-1 0v-1.5H6a.5.5 0 0 1 0-1h1.5V8a.5.5 0 0 1 .5-.5z"/>
                <path d="M8 1a2.5 2.5 0 0 1 2.5 2.5V4h-5v-.5A2.5 2.5 0 0 1 8 1zm3.5 3v-.5a3.5 3.5 0 1 0-7 0V4H1v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V4h-3.5zM2 5h12v9a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V5z"/>
              </svg>
              <p class="text-center">
                Quantity:
              </p>
              <input
                type="number" value={item.quantity}
                on:input={(event) => handleQuantityChange(item, event)}
                on:keypress={(event) => onlyNumbers(event)}
                class="input input-bordered w-1/2 max-w-xs text-center disable-spin-buttons"
                inputmode="numeric"
                pattern="[0-9]*"
                min="1"
              />
            </div>
            
            <button on:click={() => handleRemoveCartItem(item)} class="btn bg-red-500 text-white mt-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
              </svg>
              Remove
            </button>
          </div>
        {/if}
      </div>
    {/each}
  </div>
</body>
