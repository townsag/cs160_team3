<script lang='ts'>
  //array size not updating
  import { navigate } from "svelte-routing";
  import { removeCartItem, updateCartItem } from "../util/RequestController"
  import { cartItemQuantitySignal, cartItemRemovedSignal } from "../stores/CartObserver";

  export let filteredItems: any;
  export let isAdmin: Boolean;
  export let isCartItem: Boolean;

  let quantityErrorState = false;
  let quantityErrorTextState = "";
  let quantityErrorModal: HTMLDialogElement;

  $: if (quantityErrorState) {
      showQuantityErrorModal();
  }

  function showQuantityErrorModal() {
    quantityErrorModal.showModal();
  }

  function closeQuantityErrorModal() {
    quantityErrorModal.close();
    quantityErrorState = false;
  }

  function handleItemClick(item: any) {
    if (!isCartItem) {
      //navigate(`/itemView/${item.product_id}`, { state: { item } });
      navigate(`/itemView/${item.product_id}`);

      console.log("ItemDisplay: " + item.name);
    }
  }

  //let displayedItem = [];
  //displayedItem = filteredItems;
  //console.log("displayed list (in itemdisplay): " + displayedItem);

  //
  // BELOW USED IF ITEM DISPLAY IS FOR CART ITEM
  //

  // Cart Item Removal
  async function handleRemoveCartItem(item: any) {
    const result = await removeCartItem(item.cart_item_id);

    if (result.success) {
        console.log("Cart item removed successfully.");
        cartItemRemovedSignal.set(!$cartItemRemovedSignal);
    } else {
        console.error("Failed to remove cart item:", result.message);
    }
  }

  // Cart Item Quantity Change
  async function handleQuantityChange(item: any, event: any) {
    const newQuantity = parseInt(event.target.value, 10);

    if (!isNaN(newQuantity) && newQuantity <= 20) {
      try {
        const result = await updateCartItem(item.cart_item_id, item.product_id, newQuantity);

        if (result.success) {
          if (newQuantity === 0) {
            handleRemoveCartItem(item);
          }

          console.log(item.cart_item_id, item.category.name, "Cart item updated successfully: Quantity changed.");
          cartItemQuantitySignal.set(!$cartItemQuantitySignal);
        } else {
          console.error("Failed to update cart item:", result.message);
          quantityErrorTextState = result.message;
          quantityErrorState = true;
        }
      } catch (error) {
        console.log("An error occurred:", error)
        quantityErrorTextState = "An error occurred.";
        quantityErrorState = true;
      }
    } else {
      console.log("Inputted quantity is not a number less than 20.");
      quantityErrorTextState = "Inputted quantity must be more than 0 and less than 20.";
      quantityErrorState = true;
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
    min-height: 80vh;
    margin: 0;
    padding: 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
</style>

<body>
  <dialog bind:this={quantityErrorModal} class="modal">
    <div class="modal-box bg-red-300">
        <h3 class="font-bold text-lg">Error!</h3>
        <p class="py-4">{quantityErrorTextState}</p>
    </div>
    <form method="dialog" class="modal-backdrop">
        <button on:click={closeQuantityErrorModal}>close</button>
    </form>
  </dialog>

  <div class="grid-container mt-4">
    {#if isAdmin && !isCartItem}
      <div class="border p-4 rounded-lg shadow-md hover:shadow-xl transition duration-300">
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
      <div on:click={() => handleItemClick(item)} class="border p-4 rounded-lg shadow-md hover:shadow-xl transition duration-300">
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
            <div class="flex flex-wrap">
              {#each item.tags as tag (tag)}
                <span class="bg-gray-200 text-gray-800 px-2 py-1 rounded-full text-sm mr-2 mb-2">{tag.name}</span>
              {/each}
            </div>
          {/if}

          {#if isCartItem}
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <input
              type="number" value={item.quantity}
              on:input={(event) => handleQuantityChange(item, event)}
              class="input input-bordered w-full max-w-xs"
            />
            
            <button on:click={() => handleRemoveCartItem(item)} class="btn bg-red-500 text-white mt-2">Remove</button>
          {/if}

        </div>
      </div>
    {/each}
  </div>
</body>
