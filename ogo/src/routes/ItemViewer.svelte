<script lang='ts'>
    import { onMount } from 'svelte';

    let productID = window.location.href.match(/\/(\d+)$/)[1];
    console.log(productID);

    let currentUser;
    let isAdmin = false;

    let itemName = "Name";
    let itemDescription = "Description";
    let itemImgUrl = "https://cdn.vectorstock.com/i/preview-1x/98/76/plus-sign-vector-46979876.jpg";
    let itemQuantityInStock = 0;
    let itemSelectedQuantity = 0;
    let itemPrice = 0.0;
    let itemWeight = 0.0;

    /**
     * @type {{ name: any; description: any; image: any; quantity: any; price: number; weight: any; }}
     */
    let item: any;
    let finishLoading = false;

    async function sequential_api_calls(){
        try{                                  //getItemFromID
            const response = await fetch("/getProduct?productID=" + productID) 
            const data = await response.json();
            item = data;
            console.log("curItem: " + data.name);
            console.log("Product ID: " + productID);

            itemName = item.name;
            itemDescription = item.description;
            itemImgUrl = item.image;
            itemQuantityInStock = item.quantity;
            itemPrice = item.price;
            itemWeight = item.weight;
        } catch (error) {
            console.log("error: ", error);
            console.log("curItem: " + null);
            productID = "0";
            console.log("Product ID: " + productID);
        }
        try{                                  //getUser
            const response = await fetch("/getUser", { method: "GET" });
            const data = await response.json();
            currentUser = data;
            isAdmin = currentUser.is_admin;
            console.log("isAdmin: " + isAdmin);
        } catch (error) {
            console.log("error: ", error);
        }
    }

    onMount(async () => {
        sequential_api_calls();
        finishLoading = true;
    }); 
    
    function addToCart() {
        console.log("added to cart");
    }
    function buyNow() {
        console.log("buy now");
    }
    function createItem() {
        console.log("create item");
    }
    function applyChanges() {
        console.log("apply changes");
    }
</script>

<style>
    .item-container {
      min-width: 400px;
      max-width: 800px;
      gap: 10px;
      padding: 20px;
      align-self: center;
    }
  
    .main-image {
      object-fit: cover;
      align-self: center;
    }
  
    .item-details {
        max-width: 80vw;
        padding: 20px;
        object-fit: scale-down;
        align-self: center;
    }

    .midContainer {
        display: flex;
        flex-direction: column;
        min-height: 80vh; 
        width: 80%;
        align-content: center;
    }

    .bigFont {
        font-size: 95px;
        text-align: left;
        vertical-align: top;
        padding: 20px;
    }

    .mediumFont {
        font-size: 40px;
        text-align: left;
        vertical-align: top;
        padding: 20px;
    }

    .smallFont {
        font-size: 25px;
        text-align: left;
        vertical-align: top;
        padding: 20px;
    }

    .heightBig {
        height: 100px; /* Set the desired height in pixels or any other valid CSS height value */
    }

    .heightMid {
        height: 45px; /* Set the desired height in pixels or any other valid CSS height value */
    }

    .heightSmall {
        height: 30px; /* Set the desired height in pixels or any other valid CSS height value */
    }
</style>

{#if finishLoading}
    <div style="align-self: center; align-items: center;">   
        {#if isAdmin} 
            <div class="midContainer mx-auto p-2 mb-4">
                <div class="item-container">
                    <div class="border rounded-3xl shadow-md">
                        <img src={itemImgUrl} alt={itemName} class="main-image mb-2 w-full h-full object-cover"/>
                    </div>
                </div>
                <div class="item-details">
                    <table style="border: 0px solid black; width: 100%;">
                        <tr>
                            <td colspan="2">
                                <input bind:value={itemName} type="text" placeholder=itemName class="input input-bordered w-full bigFont heightBig" style="width: 100%;"/>
                            </td>
                        </tr>
                        <tr><td><div class="mb-5"></div></td></tr>
                        <tr>
                            <td colspan="2">
                                <input bind:value={itemDescription} type="text" placeholder=itemDescription class="input input-bordered w-full smallFont heightSmall" />
                            </td>
                        </tr>
                        <tr><td><div class="mb-5"></div></td></tr>
                        <tr>
                            <td colspan="2">
                                <input bind:value={itemImgUrl} type="text" placeholder=itemImgUrl class="input input-bordered w-full smallFont heightSmall" />
                            </td>
                        </tr>
                        <tr><td><div class="mb-2"></div></td></tr>
                        <tr>
                            <td style="padding-right: 40px;">
                                <label for="weightInput" class="mediumFont">Weight(lbs): </label>
                                <input bind:value={itemWeight} type="text" placeholder=itemWeight id="weightInput" class="input input-bordered w-full smallFont heightSmall" />
                            </td>
                            <td>
                                <label for="inStockInput" class="mediumFont">InStock: </label>
                                <input bind:value={itemQuantityInStock} type="text" placeholder=itemQuantityInStock id="inStockInput" class="input input-bordered w-full smallFont heightSmall" />
                            </td>
                        </tr>
                        <tr><td><div class="mb-2"></div></td></tr>
                        <tr>
                            <td colspan="2">
                                <label for="priceInput" class="mediumFont">Price($): </label>
                                <input bind:value={itemPrice} type="text" placeholder=itemPrice.toFixed(2) id="priceInput" class="input input-bordered w-full smallFont heightSmall" />
                            </td>
                        </tr>
                    </table>
                    <div class="mb-20"></div>
                    {#if productID != "0"}
                        <button class="bg-yellow-500 text-white px-6 py-3 rounded hover:bg-yellow-600 text-2xl" on:click={applyChanges}>Apply Changes</button>
                    {:else}
                        <button class="bg-yellow-500 text-white px-6 py-3 rounded hover:bg-yellow-600 text-2xl" on:click={createItem}>Create Item</button>
                    {/if}
                </div>
            </div>
        {:else} 
            <div class="midContainer mx-auto p-2 mb-4">
                <div class="item-container">
                    <div class="border rounded-3xl shadow-md">
                        <img src={itemImgUrl} alt={itemName} class="main-image mb-2 w-full h-full object-cover"/>
                    </div>
                </div>
                <div class="item-details">
                    <table style="border: 0px solid black; width: 100%;">
                        <tr>
                            <td class="bigFont" colspan="2">{itemName}</td>
                        </tr>
                        <tr>
                            <td class="smallFont" colspan="2">{itemDescription}</td>
                        </tr>
                        <tr>
                            <td class="mediumFont" style="padding-right: 50px;">Weight: {itemWeight} lbs</td>
                            <td class="mediumFont">In Stock: {itemQuantityInStock}</td>
                        </tr>
                        <tr>
                            <td class="mediumFont" style="padding-right: 50px;">Price: ${itemPrice.toFixed(2)}</td>
                            <td class="mediumFont">Quantity: {itemSelectedQuantity}</td>
                        </tr>
                    </table>
                    <div class="mb-20"></div>
                    <div style="padding-left: 20px; align-items: center;">
                        <button class="bg-yellow-500 text-white px-6 py-3 rounded hover:bg-yellow-600 text-2xl" on:click={addToCart}>Add to Cart</button>
                    </div>
                </div>
            </div>
        {/if}
    </div>
{/if}