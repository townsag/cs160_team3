<script>
    import { onMount } from 'svelte';

    let productID = "0";
    productID = window.location.href.match(/\/(\d+)$/)[1];
    console.log(productID);

    /**
     * @type {{ name: any; description: any; image: any; quantity: any; price: number; weight: any; }}
     */
    let item;
    let finishLoading = false;

    async function sequential_api_calls(){
        try{                                  //getItemFromID
            const response = await fetch("/getProduct?productID=" + productID) 
            const data = await response.json();
            item = data;
            console.log("curItem: " + data.name);
            finishLoading = true;
        } catch (error) {
            console.log("error: ", error);
        }
    }

    onMount(async () => {
        sequential_api_calls();
    }); 
    
    let image1 = "https://www.applesfromny.com/wp-content/uploads/2020/05/20Ounce_NYAS-Apples2.png";
    let image = "https://5.imimg.com/data5/SELLER/Default/2021/8/YN/SE/FV/72826034/red-apple.jpg";
    let image3 = "https://5.imimg.com/data5/AK/RA/MY-68428614/apple-500x500.jpg";
    let image2 = "https://5.imimg.com/data5/YY/EN/MY-8155364/fresh-apple-500x500.jpg";
    let image4 = "https://www.organicangels.com/pub/media/catalog/product/cache/36ab34911dcaeecf8b2210fc9d79ccec/a/d/addon_applefuji.jpg";
    let image5 = "https://www.kapruka.com/shops/specialGifts/productImages/1215060818546_apples.jpg";
    let name = "apple";
    let price = 99.99;
    const images = [image, image1, image2, image3, image4, image5];

    function addToCart() {
        console.log("added to cart");
    }
    function buyNow() {
        console.log("buy now");
    }
</script>

<style>
    .item-container {
      min-width: 400px;
      max-width: 800px;
      gap: 20px;
      margin: 20px;
      padding: 20px;
    }
  
    .main-image {
      object-fit: cover;
      align-self: center;
    }
  
    .thumbnail-container {
      display: flex;
      overflow-x: scroll;
      gap: 15px;
    }
  
    .thumbnail {
      width: 150px;
      height: width;
      object-fit: cover;
    }
  
    .item-details {
        width: 100%;
    }

    .midContainer {
        display: flex;
        flex-direction: row;
        min-height: 80vh; 
        width: 80%;
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
</style>

{#if finishLoading}
    <div class="midContainer mx-auto p-2 mb-4">
        <div class="item-container">
            <div class="border rounded-3xl shadow-md">
                <img src={item.image} alt={item.name} class="main-image mb-2 w-full h-full object-cover"/>
            </div>
            <div class="mb-4"></div>
            <div class="thumbnail-container">
                {#each images as image (image)}
                <img src={image} alt="Thumbnail" class="thumbnail" />
                {/each}
            </div>
        </div>
    
        <div class="item-details">
            <table style="border: 0px solid black; width: 100%;">
                <tr>
                    <td class="bigFont" colspan="2">{item.name}</td>
                </tr>
                <tr>
                    <td class="smallFont" colspan="2">{item.description}</td>
                </tr>
                <tr>
                    <td class="mediumFont" colspan="2">Weight: {item.weight} lbs</td>
                </tr>
                <tr>
                    <td class="mediumFont" style="padding-right: 50px;">Price: ${item.price.toFixed(2)}</td>
                    <td class="mediumFont">Quantity: {"quantity"}</td>
                </tr>
            </table>
            <div class="mb-20"></div>
            <table style="border: 0px solid black; width: 100%;">
                <tr>
                    <td style="padding-left: 20px; display: flex; align-items: center;"><button class="bg-yellow-500 text-white px-6 py-3 rounded hover:bg-yellow-600 text-2xl" on:click={addToCart}>Add to Cart</button></td>
                    <td><button style="display: flex; align-items: center;" class="bg-yellow-500 text-white px-6 py-3 rounded hover:bg-yellow-600 text-2xl" on:click={buyNow}>Buy Now</button></td>
                </tr>
            </table>
        </div>
    </div>
{/if}