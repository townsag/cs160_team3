<script lang="ts">
    import { navigate } from "svelte-routing/src/history";
    import { getCart, getCurrentUser, removeCartItem, placeOrder } from "../lib/util/RequestController"
    import { onMount } from "svelte";
    
    import Navbar from "../lib/components/Navbar.svelte";
    import { alert } from '../lib/stores/alertStore';
    import AlertDaisy from "../lib/components/AlertDaisy.svelte";

    // 0.0724776501?
    const TAX_RATE = 0.0725;

    let fullNameState = "";
    let cardHolderNameState = "";
    let cardNumberState = "";
    let phoneNumberState = "";
    let cardExpiryState = "";
    let cardCvcState = "";

    let price = 0

    async function removeAllCartItems(cartData: any) {
    const removalPromises = cartData.items.map(async (item: any) => {
            const removalResult = await removeCartItem(item.cart_item_id);
            return removalResult;
        });

        // Wait for all removal promises to resolve
        const removalResults = await Promise.all(removalPromises);

        // Check if all removals were successful
        const allRemovalsSuccessful = removalResults.every(result => result.success);

        if (allRemovalsSuccessful) {
            console.log("All cart items removed successfully.");
        } else {
            console.error("Failed to remove one or more cart items.");
        }
    }

    let cartData = {}
    let shipping = 0
    let userAddress = ""
    onMount(async ()=>{
        cartData = await getCart()
        let userData = await getCurrentUser()
        userAddress = userData.user.address
        if(!userAddress) userAddress = "None Set Please See Settings Page"
        const totalCost = cartData.cart.items.reduce((acc: any, item: any) => {
            return acc + item.price * item.quantity;
        }, 0);
        const totalWeight = cartData.cart.items.reduce((acc: any, item: any) => {
            return acc + item.weight * item.quantity;
        }, 0);
        if(totalWeight > 20) shipping = 10
        price = totalCost
    });

    async function handlePaymentSubmit() {
        let failedCondition = "";

        switch (true) {
            case !fullNameState || !/^[a-zA-Z\s]+$/.test(fullNameState):
                failedCondition = "Full Name";
                break;
            case !cardHolderNameState || !/^[a-zA-Z\s]+$/.test(cardHolderNameState):
                failedCondition = "Card Holder Name";
                break;
            case !cardNumberState || !/^\d{16}$/.test(cardNumberState):
                failedCondition = "Card Number";
                break;
            case !phoneNumberState || !/^\(\d{3}\)-?\d{3}-?\d{4}$/.test(phoneNumberState):
                failedCondition = "Phone Number";
                break;
            case !cardExpiryState || !/^\d{2}\/\d{2}$/.test(cardExpiryState):
                failedCondition = "Card Expiry (MM/YY)";
                break;
            case !cardCvcState || !/^\d+$/.test(cardCvcState):
                failedCondition = "Card CVC";
                break;
            case userAddress === "None Set Please See Settings Page":
                failedCondition = "Check Address";
                break;
            default:
                failedCondition = null;
        }

        if (failedCondition) {
            alert.set({ show: true, message: `Invalid input for ${failedCondition}`, type: 'warning'});
            return;
        }

        removeAllCartItems(cartData.cart);
        const res = await placeOrder(cartData.cart.items)
        if(res.success == true)  {
            alert.set({ show: true, message: `Order placed`, type: 'success'});
            navigate("/browse");
        } else {
            failedCondition = "Could not Place order";
            alert.set({ show: true, message: failedCondition, type: 'error'});
        }
        return;
    }
</script>

<style>
    .midContainer {
        display: flex;
        flex-direction: column;
        min-height: 80vh; 
    }

    @media (min-width: 1000px) {
        .midContainer {
            flex-direction: row; /* Display items side by side */
        }
    }
</style>

<html lang="en" data-theme="lemonade">
    <Navbar/>
    <AlertDaisy {alert} />
    <div class="midContainer">
        <div class="basis-1/2">
            <div class="card bg-base-100 border-2 border-black-500 m-8 mb-4 lg:mb-8 lg:mr-4 shadow-md" >
                <div class="card-body">
                    <h1 class="card-title mb-4">MAKE PAYMENT</h1>
                    <div class="form-control w-full">
                        <!-- svelte-ignore a11y-label-has-associated-control -->
                        <label class="label">
                            <span class="label-text">Full Name </span>
                        </label>
                        <input bind:value={fullNameState} type="text" class="input input-bordered w-full " placeholder="John Papper"/>
                        <!-- svelte-ignore a11y-label-has-associated-control -->
                        <label class="label">
                            <span class="label-text">Phone Number </span>
                        </label>
                        <input bind:value={phoneNumberState} type="text" class="input input-bordered w-full " placeholder="(999)-999-9999"/>
                        <!-- svelte-ignore a11y-label-has-associated-control -->
                        <label class="label">
                            <span class="label-text">Address</span>
                        </label>
                        <div class="inline-block ml-1">
                            <p class="text-base">{userAddress}</p>
                        </div>
                        <div class="inline-block ml-1">
                            <a class="text-xs underline mt-2" href="/settings">User Settings</a>
                        </div>
                        <!-- svelte-ignore a11y-label-has-associated-control -->
                        <label class="label">
                            <span class="label-text">Card</span>
                        </label>
                        <input bind:value={cardHolderNameState} type="text" class="input input-bordered w-full " placeholder="Card Holder Name"/>
                        <input bind:value={cardNumberState} type="text" class="input input-bordered w-full mt-2" placeholder="Card Number No Dashes"/>
                        <div id="notfull" class="flex justify-between mt-2">
                            <div class="flex-1 mr-1">
                                <input bind:value={cardExpiryState} type="text" class="input input-bordered w-full " placeholder="Expiry Date"/>
                            </div>
                            <div class="flex-1 ml-1" >
                                <input bind:value={cardCvcState} type="text" class="input input-bordered w-full " placeholder="CVC Code"/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="basis-1/2">
            <div class="card bg-base-100 border-2 border-black-500 m-8 mt-4 lg:mt-8 lg:ml-4 shadow-md">
                <div class="card-body">
                    <h1 class="card-title mb-4">ORDER PRICE</h1>

                    <div class="flex flex-row">
                        <div class="basis-1/2">
                            <p class="text-left"><b>Cart:</b></p>
                            <p class="text-left"><b>Tax:</b></p>
                            <p class="text-left"><b>Shipping:</b></p>
                            <p class="text-left"><b>Total:</b></p>
                        </div>

                        <div class="basis-1/2">
                            <p class="text-right">${(price).toFixed(2)}</p>
                            <p class="text-right">${(price * TAX_RATE).toFixed(2)}</p>
                            <p class="text-right">${shipping}</p>
                            <p class="text-right">${(shipping + (price * TAX_RATE) + price).toFixed(2)}</p>
                        </div>
                    </div>
                    <button on:click={handlePaymentSubmit} class="btn bg-secondary mt-6">Pay Now</button>
                </div>
            </div>
        </div>
    </div>
</html>
