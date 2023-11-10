<script lang='ts'>
    import { onMount } from 'svelte';
    import { navigate } from 'svelte-routing';

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
        //console.log(toggleTagsList);
    }

    async function sequential_api_calls(){
        try{                                  //getUser
            const response = await fetch("/getUser", { method: "GET" });
            const data = await response.json();
            currentUser = data;
            isAdmin = currentUser.is_admin;
            //console.log("isAdmin: " + isAdmin);
        } catch (error) {
            console.log("error: ", error);
        }
        try{                                  //getAllTags
            const response = await fetch("/getTags", { method: "GET" });
            const data = await response.json();
            allTagsList = data;
            //console.log("allTagsList: " + data);
            loadedTags = true;
        } catch (error) {
            console.log("error: ", error);
        }
        try{                                  //getAllCategories
            const response = await fetch("/getCategories", { method: "GET" });
            const data = await response.json();
            allCategoriesList = data;
            //console.log("allCategoriesList: " + data);
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

            for (let i = 0; i < item.tags.length; i++) {
                itemTags[i] = item.tags[i].name;
                //console.log("Added tag: " + item.tags[i].name);
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
            //console.log(allTagsList.length);
            toggleTagsList = new Array(allTagsList.length);
            for (let i = 0; i < toggleTagsList.length; i++) {
                toggleTagsList[i] = false;
            }
            //console.log(itemTags);
            if (itemTags.length != 0) {
                for (let i = 0; i < itemTags.length ; i++) {
                    toggleTag(itemTags[i]);
                }
            }
            //console.log("Not Displayed: " + toggleTagsList);
            loadedTags = false;
            loadedRealTags = false;
            finishLoading = true;
        }
    }

    async function createProduct() {
        /*
        console.log(itemName);
        console.log(itemDescription);
        console.log(itemImgUrl);
        console.log(itemQuantityInStock);
        console.log(itemPrice);
        console.log(itemWeight);
        console.log(itemCategoryID);
        console.log(toggleTagsListID); */
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
            alert("Created item: " + itemName);
            returnToBrowse();
		} else {
            const message = await createProductResponse.text();
			console.error("Error creating product:", message);
            alert("Cannot created item: " + itemName);
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
            alert("Updated item: " + itemName);
            returnToBrowse();
		} else {
            const message = await updateProductResponse.text();
			console.error("Error updating product:", message);
            alert("Cannot update item: " + message);
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
            alert("Added " + itemSelectedQuantity + " " + itemName);
            returnToBrowse();
		} else {
            const message = await updateProductResponse.text();
			console.error("Error adding to cart:", message);
            alert("Cannot add item: " + message);
		}
	}

    function returnToBrowse() {
        navigate("/browse");
    }
    
    function addToCart() {
        if (itemSelectedQuantity != 0) {
            addItemToCart();
        }
        //console.log("added to cart");
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
        handleApplyChanges();
    }
</script>

<style>
    .item-container {
        min-width: 30vw;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 30vh;
    }
  
    .main-image {
        object-fit: cover;
        align-self: center;
    }
  
    .item-details {
        max-width: 80vw;
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

    .tagScroll {
        display: flex;
        flex-direction: column;
        height: 60%; 
        align-content: center;
        justify-content: space-between;
        overflow-y: scroll;
        border: 1px solid gray;
        width: 100%
    }

    .tableTest {
        align-content: center;
        justify-content: space-between;
        border: 0px solid black;
        width: 80vw;
        border-collapse: collapse;
        padding: 10px;
    }

    .tableTest td {
        text-align: right; /* Align text inside cells to the left */
        vertical-align: middle;
        border: 0px solid black;
        padding: 10px;
    }

    td {
        padding: 10px;
        border: 0px solid black;
    }

    .column1 {
        width: 70%;
    }

    .column2 {
        width: 25%; 
    }

    .columnSpacer {
        width: 5%; 
    }
</style>

{#if finishLoading}
    <div style="align-self: center; align-items: center;">   
        {#if isAdmin} 
            <div class="midContainer mx-auto p-2 mb-4">
                <table class="tableTest">
                    <tr>
                        <td class="column1" rowspan="2" style="text-align: center;">
                            <div class="item-container">
                                <div class="border rounded-3xl shadow-md" style="width: 65%;">
                                    <img src={itemImgUrl} alt={itemName} class="main-image w-full h-full object-cover"/>
                                </div>
                            </div>
                        </td>
                        <td class="columnSpacer"></td>
                        <td class="column2" style="text-align: left;">
                            <div class="filter-item">
                                <label for="categoryDropDown" class="">Category: </label>
                                {#if productID != "0"}
                                    <select bind:value={itemCategory} style="border: 1px solid gray; width: 100%;" id="categoryDropDown" on:change={handleCategoryChange}>
                                        {#each allCategoriesList as category}
                                            <option value={category.name}>{category.name}</option>
                                        {/each}
                                    </select>
                                {:else}
                                    <select style="border: 1px solid gray; width: 100%;" id="categoryDropDown" on:change={handleCategoryChange}>
                                        {#each allCategoriesList as category}
                                            <option value={category.name}>{category.name}</option>
                                        {/each}
                                    </select>
                                {/if}
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td></td>
                        <td style="text-align: left;">
                            <label for="tagInput" class="">Tags:</label>
                            <div class="tagScroll">
                                {#each allTagsList as tag, index}
                                    <label class="" style="padding: 5px;">
                                        {tag.name}
                                        {#if productID != "0"}
                                            <input type="checkbox" on:change={() => toggleTag(tag.name)} bind:checked={toggleTagsList[index]}/>
                                        {:else}
                                            <input type="checkbox" on:change={() => toggleTag(tag.name)} bind:checked={toggleTagsList[index]}/>
                                        {/if}
                                    </label>
                                {/each}
                            </div>
                        </td>
                    </tr>
                    <tr><td><div style="padding-top: 20px;"></div></td></tr>
                    <tr>
                        <td>
                            <label for="nameInput" class="">Name: </label>
                            <input id="nameInput" bind:value={itemName} type="text" placeholder=itemName class="input input-bordered heightSmall" style="width: 85%;"/>
                        </td>
                        <td></td>
                        <td>
                            <label for="weightInput" class="">Weight(lbs): </label>
                            <input id="weightInput" bind:value={itemWeight} type="number" placeholder=itemWeight class="input input-bordered heightSmall" style="width: 40%;"/>
                        </td>
                        
                    </tr>
                    <tr>
                        <td>
                            <label for="descInput" class="">Description: </label>
                            <input id="descInput" bind:value={itemDescription} type="text" placeholder=itemDescription class="input input-bordered heightSmall" style="width: 85%;"/>
                        </td>
                        <td></td>
                        <td>
                            <label for="inStockInput" class="">In Stock: </label>
                            <input id="inStockInput" bind:value={itemQuantityInStock} type="number" placeholder=itemQuantityInStock class="input input-bordered heightSmall" style="width: 40%;"/>
                        </td>
                        
                    </tr>
                    <tr>
                        <td>
                            <label for="urlInput" class="">URL: </label>
                            <input id="urlInput" bind:value={itemImgUrl} type="text" placeholder=itemImgUrl class="input input-bordered heightSmall" style="width: 85%;"/>
                        </td>
                        <td></td>
                        <td>
                            <label for="priceInput" class="">Price($): </label>
                            <input id="priceInput" bind:value={itemPrice} type="number" placeholder=itemPrice.toFixed(2) class="input input-bordered heightSmall" style="width: 40%;"/>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-top: 40px;">
                            {#if productID != "0"}
                                <button style="width: 90%;" class="bg-green-500 text-white px-6 py-3 rounded hover:bg-green-600 text-2xl" on:click={applyChanges}>Apply Changes</button>
                            {:else}
                                <button style="width: 90%;" class="bg-green-500 text-white px-6 py-3 rounded hover:bg-green-600 text-2xl" on:click={createItem}>Create Item</button>
                            {/if}
                        </td>
                        <td></td>
                        <td style="padding-top: 40px;">
                            <button style="width: 90%;" class="bg-red-500 text-white px-6 py-3 rounded hover:bg-red-600 text-2xl" on:click={returnToBrowse}>Cancel</button>
                        </td>
                    </tr>
                </table>
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
                            <td>
                                <label for="quantityInput" class="">Quantity: </label>
                                <input id="quantityInput" bind:value={itemSelectedQuantity} type="number" placeholder=itemSelectedQuantity class="input input-bordered heightSmall" style="width: 40%;"/>
                            </td>
                        </tr>
                    </table>
                    <div class="mb-20"></div>
                    <div style="padding-left: 20px; align-items: center;">
                        {#if productID != "0"}
                            <button class="bg-green-500 text-white px-6 py-3 rounded hover:bg-green-600 text-2xl" on:click={addToCart}>Add to Cart</button>
                        {/if}
                    </div>
                </div>
            </div>
        {/if}
    </div>
{/if}