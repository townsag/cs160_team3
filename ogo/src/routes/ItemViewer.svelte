<script lang='ts'>
    import { onMount } from 'svelte';
    import { navigate } from 'svelte-routing';
    import Navbar from "../lib/components/Navbar.svelte";

    import { alert } from '../lib/stores/alertStore';
    import AlertDaisy from "../lib/components/AlertDaisy.svelte";

    let productID = window.location.href.match(/\/(\d+)$/)[1];
    console.log(productID);

    let currentUser;
    let isAdmin = false;

    let itemName = "";
    let itemDescription = "";
    let itemImgUrl = "";
    let itemQuantityInStock = 0;
    let itemSelectedQuantity = 1;
    let itemPrice = 0.0;
    let itemWeight = 0.0;

    /**
     * @type {{ name: any; description: any; image: any; quantity: number; price: number; weight: number; category: any; tags: any;}}
     */
    let item: any;
    let finishLoading = false;

    let allTagsList: any[] = [];
    let allCategoriesList: any[] = [];

    let itemCategory: string = "";
    let itemCategoryID = 0;
    let toggleTagsList: any[] = [];
    let toggleTagsListID: any[] = [];
    let itemTags: any[] = [];
    let loadedTags = false;
    let loadedRealTags = false;
    
    function handleCategoryChange(event: any) {
        itemCategory = event.target.value;
    }

    function toggleTag(tagName: string) {
        for (let i = 0; i < allTagsList.length; i++) {
            if (allTagsList[i].name == tagName) {
                toggleTagsList[i] = !toggleTagsList[i];
            }
        }
    }

    async function sequential_api_calls(){
        try{                                  //getUser
            const response = await fetch("/getUser", { method: "GET" });
            const data = await response.json();
            currentUser = data;
            isAdmin = currentUser.is_admin;
        } catch (error) {
            console.log("error: ", error);
        }
        try{                                  //getAllTags
            const response = await fetch("/getTags", { method: "GET" });
            const data = await response.json();
            allTagsList = data;
            loadedTags = true;
        } catch (error) {
            console.log("error: ", error);
        }
        try{                                  //getAllCategories
            const response = await fetch("/getCategories", { method: "GET" });
            const data = await response.json();
            allCategoriesList = data;
        } catch (error) {
            console.log("error: ", error);
        }
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
            itemCategory = item.category.name;
            itemSelectedQuantity = 1;

            for (let i = 0; i < item.tags.length; i++) {
                itemTags[i] = item.tags[i].name;
            }
            console.log(itemTags);
            loadedRealTags = true;
        } catch (error) {
            console.log("error: ", error);
            console.log("curItem: " + null);
            productID = "0";
            console.log("Product ID: " + productID);
        }
    }

    onMount(async () => {
        sequential_api_calls();  
    }); 

    $: {
        if ((loadedTags && loadedRealTags && productID != "0") || (loadedTags && productID == "0")) {
            toggleTagsList = new Array(allTagsList.length);
            for (let i = 0; i < toggleTagsList.length; i++) {
                toggleTagsList[i] = false;
            }
            if (itemTags.length != 0) {
                for (let i = 0; i < itemTags.length ; i++) {
                    toggleTag(itemTags[i]);
                }
            }
            loadedTags = false;
            loadedRealTags = false;
            finishLoading = true;
        }

        if (itemPrice < 0) {
            itemPrice = 0;
        }
        if (itemWeight < 0) {
            itemWeight = 0;
        }
        if (itemQuantityInStock < 0) {
            itemQuantityInStock = 0;
        }
        if (itemSelectedQuantity < 0) {
            itemSelectedQuantity = 0;
        }

        itemPrice = Number(itemPrice.toFixed(2));
        itemWeight = Number(itemWeight.toFixed(2));

        if (itemSelectedQuantity > itemQuantityInStock) {
            itemSelectedQuantity = itemQuantityInStock;
        }
    }

    async function createProduct() {
        const createProductResponse = await fetch("/createProduct", {
            method: "POST",
            headers: {
            'Content-Type': "application/json"
            },
            body: JSON.stringify({
                "name": itemName,
                "description": itemDescription,
				"image": itemImgUrl,
				"quantity": itemQuantityInStock,
				"price": itemPrice, 
				"weight": itemWeight,
                "category_id": itemCategoryID,
                "tags": toggleTagsListID
            })
        })
		if (createProductResponse.ok) {
			const message = await createProductResponse.text();
			console.log(message);
            alert.set({ show: true, message: 'Created item: ' + itemName, type: 'success'});
            returnToBrowse();
		} else {
            const message = await createProductResponse.text();
			console.error("Error creating product:", message);
            alert.set({ show: true, message: 'Error creating product: ' + message, type: 'error'});
		}
	}
    async function handleApplyChanges() {
        const updateProductResponse = await fetch("/updateProduct", {
            method: "POST",
            headers: {
            'Content-Type': "application/json"
            },
            body: JSON.stringify({
                "product_id": parseInt(productID),
                "name": itemName,
                "description": itemDescription,
				"image": itemImgUrl,
				"quantity": itemQuantityInStock,
				"price": itemPrice, 
				"weight": itemWeight,
                "category_id": itemCategoryID,
                "tags": toggleTagsListID
            })
        })
		if (updateProductResponse.ok) {
			const message = await updateProductResponse.text();
			console.log(message);
            alert.set({ show: true, message: 'Updated item: ' + itemName, type: 'success'});
            returnToBrowse();
		} else {
            const message = await updateProductResponse.text();
			console.error("Error updating product:", message);
            alert.set({ show: true, message: 'Error updating product: ' + message, type: 'error'});
		}
	}
    async function addItemToCart() {
		const updateProductResponse = await fetch("/addCartItem", {
            method: "POST",
            headers: {
            'Content-Type': "application/json"
            },
            body: JSON.stringify({
                "product_id": parseInt(productID),
                "quantity": itemSelectedQuantity
            })
        })
		if (updateProductResponse.ok) {
			const message = await updateProductResponse.text();
			console.log(message);
            alert.set({ show: true, message: 'Added ' + itemSelectedQuantity + ' ' + itemName, type: 'success'});
            returnToBrowse();
		} else {
            const message = await updateProductResponse.text();
			console.error("Error adding to cart:", message);
            alert.set({ show: true, message: 'Error adding to cart: ' + message, type: 'error'});
		}
	}

    function returnToBrowse() {
        navigate("/browse");
    }
    
    function addToCart() {
        if (!Number.isInteger(itemSelectedQuantity)) {
            alert.set({ show: true, message: 'Quantity must be an integer', type: 'warning'});
            return;
        }
        if (itemSelectedQuantity <= 0) {
            alert.set({ show: true, message: 'Quantity must be greater than 0', type: 'warning'});
            return;
        }
        addItemToCart();
    }
    function createItem() {
        toggleTagsListID.length = 0;
        itemCategoryID = 0;
        for (let i = 0; i < allCategoriesList.length; i++) {
            if (itemCategory == allCategoriesList[i].name) {
                itemCategoryID = i;
            }
        }
        itemCategoryID += 1;
        for (let i = 0; i < toggleTagsList.length; i++) {
            if (toggleTagsList[i] == true) {
                toggleTagsListID.push(i + 1);
            }
        }
        if (itemName.length == 0 || itemDescription.length == 0 || itemImgUrl.length == 0) {
            alert.set({ show: true, message: 'Item must have name, description, and image URL', type: 'warning'});
            return;
        }
        if (itemPrice <= 0 || itemWeight <= 0) {
            alert.set({ show: true, message: 'Weight and price must be greater than 0', type: 'warning'});
            return;
        }
        if (!Number.isInteger(itemQuantityInStock)) {
            alert.set({ show: true, message: 'Quantity must be an integer', type: 'warning'});
            return;
        }
        createProduct();
    }
    function applyChanges() {
        toggleTagsListID.length = 0;
        itemCategoryID = 0;
        for (let i = 0; i < allCategoriesList.length; i++) {
            if (itemCategory == allCategoriesList[i].name) {
                itemCategoryID = i;
            }
        }
        itemCategoryID += 1;
        for (let i = 0; i < toggleTagsList.length; i++) {
            if (toggleTagsList[i] == true) {
                toggleTagsListID.push(i + 1);
            }
        }
        if (itemName.length == 0 || itemDescription.length == 0 || itemImgUrl.length == 0) {
            alert.set({ show: true, message: 'Item must have name, description, and image URL', type: 'warning'});
            return;
        }
        if (itemPrice <= 0 || itemWeight <= 0) {
            alert.set({ show: true, message: 'Weight and price must be greater than 0', type: 'warning'});
            return;
        }
        if (!Number.isInteger(itemQuantityInStock)) {
            alert.set({ show: true, message: 'Quantity must be an integer', type: 'warning'});
            return;
        }
        handleApplyChanges();
    }
</script>

<style>
    .main-image {
        object-fit: cover;
        align-self: center;
    }

    .midContainer {
        display: flex;
        flex-direction: column;
        min-height: 80vh; 
        width: 80%;
        align-content: center;
        margin: auto;
    }

    @media (min-width: 1000px) {
        /* Apply styles when the screen width is 768 pixels or more */
        .midContainer {
            flex-direction: row; /* Display items side by side */
        }

        table:first-child {
            width: 60%; /* First table takes 60% of the container's width */
            margin-top: 5vh;
        }

        table:last-child {
            width: 35%; /* Second table takes 35% of the container's width */
            margin-top: 5vh;
        }

        .midContainer .testMargin {
            margin-right: 30px;
        }
    }

    .testMargin {
        margin-right: 0px;
    }

    .tagScroll {
        display: flex;
        flex-direction: column;
        height: 60%; 
        align-content: center;
        justify-content: space-between;
        overflow-y: scroll;
        border: 1px solid lightgray;
        width: 100%
    }

    td {
        padding: 10px;
        border: 0px solid black;
    }
</style>

{#if finishLoading}
    <Navbar/>
    <AlertDaisy {alert} />
    <div style="align-self: center; align-items: center;">   
        {#if isAdmin} 
            <div class="midContainer mx-auto p-2 mb-4">
                <table class="testMargin" style="border: width: 100%; height: 60vh;">
                    <tr>
                        <td  colspan="2" style="height: 40vh;">
                            <div class="border rounded-3xl shadow-md" style="min-height:50%; height: 100%;">
                                <img src={itemImgUrl} alt={itemName} class="main-image w-full h-full object-cover"/>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td style="width: 20%">
                            <label for="nameInput" class="text-3xl font-semibold">Name: </label>
                        </td>
                       <td>
                            <input id="nameInput" bind:value={itemName} type="text" class="input input-bordered text-3xl font-semibold" style="width: 100%;"/>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="descInput" class="text-xl font-normal">Description: </label>
                        </td>
                        <td>
                            <input id="descInput" bind:value={itemDescription} type="text" class="input input-bordered heightSmall text-xl font-normal" style="width: 100%;"/>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="urlInput" class="text-xl font-normal">URL: </label>
                        </td>
                        <td>
                            <input id="urlInput" bind:value={itemImgUrl} type="text" class="input input-bordered heightSmall text-xl font-normal" style="width: 100%;"/>
                        </td>
                    </tr>
                </table>
                <table style="border: width: 100%; height: 100%; min-height: 30vh">
                    <tr>
                        <td colspan="2">
                            <div class="filter-item">
                                <label for="categoryDropDown" class="text-xl font-normal">Category: </label>
                                {#if productID != "0"}
                                    <select class="select text-xl font-normal rounded-lg" bind:value={itemCategory} style="border: 1px solid lightgray; width: 100%;" id="categoryDropDown" on:change={handleCategoryChange}>
                                        {#each allCategoriesList as category}
                                            <option class="text-xl font-normal" value={category.name}>{category.name}</option>
                                        {/each}
                                    </select>
                                {:else}
                                    <select class="select text-xl font-normal rounded-lg" style="border: 1px solid lightgray; width: 100%;" id="categoryDropDown" on:change={handleCategoryChange}>
                                        {#each allCategoriesList as category}
                                            <option class="text-xl font-normal" value={category.name}>{category.name}</option>
                                        {/each}
                                    </select>
                                {/if}
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            <label for="tagInput" class="text-xl font-normal">Tags:</label>
                            <div class="tagScroll rounded-lg" style="min-height: 10vh;">
                                {#each allTagsList as tag, index}
                                    <div class="form-control hover:bg-gray-100 px-2 py-1">
                                        <label class="label cursor-pointer text-xl font-normal" style="padding: 5px;">
                                          <span class="label-text text-xl font-normal">{tag.name}</span> 
                                          <input type="checkbox" class="checkbox checkbox-primary" on:change={() => toggleTag(tag.name)} bind:checked={toggleTagsList[index]}/>
                                        </label>
                                    </div>
                                {/each}
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="weightInput" class="text-xl font-normal">Weight(lbs): </label>
                        </td>
                        <td>
                            <input id="weightInput" bind:value={itemWeight} type="number" class="input input-bordered heightSmall text-xl font-normal" style="width: 100%;"/>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="priceInput" class="text-xl font-normal text-green-600 font-semibold">Price($): </label>
                        </td>
                        <td>
                            <input id="priceInput" bind:value={itemPrice} type="number" class="input input-bordered heightSmall text-xl font-normal text-green-600 font-semibold" style="width: 100%;"/>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="inStockInput" class="text-xl font-normal">In Stock: </label>
                        </td>
                        <td>
                            <input id="inStockInput" bind:value={itemQuantityInStock} type="number" class="input input-bordered heightSmall text-xl font-normal" style="width: 100%;"/>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-top: 40px; width: 50%">
                            {#if productID != "0"}
                                <button style="width: 90%;" class="btn bg-primary text-white rounded-xl text-xl" on:click={applyChanges}>Apply</button>
                            {:else}
                                <button style="width: 90%;" class="btn bg-primary text-white rounded-xl text-xl" on:click={createItem}>Create</button>
                            {/if}
                        </td>
                        <td style="padding-top: 40px; text-align: right;">
                            <button style="width: 90%;" class="btn bg-red-500 text-white rounded-xl text-xl" on:click={returnToBrowse}>Cancel</button>
                        </td>
                    </tr>
                </table>
            </div>
        {:else} 
            <div class="midContainer mx-auto p-2 mb-4">
                <table class="testMargin" style="border: width: 100%; height: 60vh;">
                    <tr>
                        <td style="height: 40vh;">
                            <div class="border rounded-3xl shadow-md" style="min-height:50%; height: 100%;">
                                <img src={itemImgUrl} alt={itemName} class="main-image w-full h-full object-cover"/>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <h2 class="text-3xl font-semibold">{itemName}</h2>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <p class="text-xl font-normal">{itemDescription}</p>
                        </td>
                    </tr>
                    <tr>
                        <td class="" style="word-wrap: break-word;">
                            <span class="bg-primary text-white px-2 py-1 rounded-full text-base mr-2 mb-2">{itemCategory}</span>
                            {#each allTagsList as tag}
                                <span class="bg-gray-200 text-gray-800 px-2 py-1 rounded-full text-base mr-2 mb-2">{tag.name}</span>
                            {/each}
                        </td>
                    </tr>
                </table>
                <table style="border: width: 100%; height: 100%;">
                    <tr>
                        <td style="width: 45%;">
                            <p class="text-xl font-normal">Weight: {itemWeight.toFixed(2)} lbs</p>
                        </td>
                        <td>
                            <p class="text-xl font-normal">Total: {(itemWeight * itemSelectedQuantity).toFixed(2)} lbs</p>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <p class="text-xl font-normal text-green-600 font-semibold">Price: ${itemPrice.toFixed(2)}</p>
                        </td>
                        <td>
                            <p class="text-xl font-normal text-green-600 font-semibold">Total: ${(itemPrice * itemSelectedQuantity).toFixed(2)}</p>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <p class="text-xl font-normal">In Stock: {itemQuantityInStock}</p>
                        </td>
                        <td>
                            <label for="quantityInput" class="text-xl font-normal">Quantity: </label>
                            <input id="quantityInput" bind:value={itemSelectedQuantity} type="number" class="input input-bordered heightSmall" style="width: 40%;"/>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            <div style="align-items: center;">
                                {#if productID != "0"}
                                    {#if itemQuantityInStock == 0}
                                        <button style="width: 100%;" disabled="disabled" class="btn bg-primary text-white mt-3 rounded-xl text-2xl" on:click={addToCart}>Add to Cart</button>
                                    {:else}
                                        <button style="width: 100%;" class="btn bg-primary text-white mt-3 rounded-xl text-2xl" on:click={addToCart}>Add to Cart</button>
                                    {/if}
                                {/if}
                            </div>
                        </td>
                    </tr>
                </table>
            </div>
        {/if}
    </div>
{/if}