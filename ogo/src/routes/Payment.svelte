<script lang="ts">
    import { navigate } from "svelte-routing/src/history";
    import { getCart, getCurrentUser, removeCartItem } from "../lib/util/RequestController"
    import { onMount } from "svelte";


    let fullNameState = "";
    let cardHolderNameState = "";
    let cardNumberState = "";
    let addressLineOneState = "";
    let addressLineTwoState = "";
    let phoneNumberState = "";
    let cityState = "";
    let stateState = ""; // this is the State locations state
    let zipCodeState = "";
    let countryState = ""; 
    let cardExpiryState = "";
    let cardCvcState = "";

    let price = 0

    async function removeAllCartItems(cartData) {
    const removalPromises = cartData.items.map(async (item) => {
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
        const totalCost = cartData.cart.items.reduce((acc, item) => {
            return acc + item.price * item.quantity;
        }, 0);
        const totalWeight = cartData.cart.items.reduce((acc, item) => {
            return acc + item.weight * item.quantity;
        }, 0);
        if(totalWeight > 20) shipping = 20
        price = totalCost
    });
    

    let paymentErrorState = false;
    let paymentErrorTextState = "";
    let paymentErrorModal: HTMLDialogElement;

    $: if (paymentErrorState) {
        showPaymentErrorModal();
    }

    function showPaymentErrorModal() {
        paymentErrorModal.showModal();
    }

    function closePaymentErrorModal() {
        paymentErrorModal.close();
        paymentErrorState = false;
    }

    async function handlePaymentSubmit() {
        if (
            (!fullNameState || !/^[a-zA-Z]+$/.test(fullNameState)) ||
            (!cardHolderNameState || !/^[a-zA-Z]+$/.test(cardHolderNameState)) ||
            (!cardNumberState || !/^\d+$/.test(cardNumberState) || cardNumberState.length != 16) ||
            (!phoneNumberState || !/^\d+$/.test(phoneNumberState)) ||
            (!cardExpiryState || !/^\d+$/.test(cardExpiryState)) ||
            (!cardCvcState || !/^\d+$/.test(cardCvcState))
        ) {
            paymentErrorTextState = "Please check all the required fields.";
            paymentErrorState = true;
            return;
        }
        removeAllCartItems(cartData.cart)
        // navigate("/browse")
        console.log(await getCart())
    }
</script>

<html lang="en" data-theme="lemonade">
    <div class="flex">
        <div class="relative min-w-screen h-screen items-left px-4 sm:px-0 pt-1">
            <div class="absolute inset-0 bg-white bg-opacity-50 backdrop-blur-md backdrop-contrast-125"></div>
            <div class="card w-full  md:w5/5 xl:w-100 bg-base-100 border-2 border-black-500 mt-8">
                <dialog bind:this={paymentErrorModal} class="modal">
                    <div class="modal-box bg-red-300">
                        <h3 class="font-bold text-lg">Payment Error!</h3>
                        <p class="py-4">{paymentErrorTextState}</p>
                    </div>
                    <form method="dialog" class="modal-backdrop">
                        <button on:click={closePaymentErrorModal}>close</button>
                    </form>
                </dialog>
                <div class="card-body pl-20 pr-20 pt-10">
                    <h1 class="card-title">Make Payment</h1>
                    <div class="form-control w-full">
                        <label class="label">
                            <span class="label-text">Full Name </span>
                        </label>
                        <input bind:value={fullNameState} type="text" class="input input-bordered w-full " placeholder="John Papper"/>
                        <label class="label">
                            <span class="label-text">Phone Number </span>
                        </label>
                        <input bind:value={phoneNumberState} type="text" class="input input-bordered w-full " placeholder="(999)-999-9999"/>
                        <label class="label">
                            <span class="label-text">Address</span>
                        </label>
                        <input bind:value={addressLineOneState} type="text" class="input input-bordered w-full " placeholder={userAddress} readonly/>
                        <a class="text-xs underline" href="/settings">User Settings</a>
                        <label class="label">
                            <span class="label-text">Card</span>
                        </label>
                        <input bind:value={cardHolderNameState} type="text" class="input input-bordered w-full " placeholder="Card Holder Name"/>
                        <input bind:value={cardNumberState} type="text" class="input input-bordered w-full " placeholder="Card Number"/>
                        <div id="notfull" class="flex justify-between">
                            <div class="flex-1 ">
                                <input bind:value={cardExpiryState} type="text" class="input input-bordered w-full " placeholder="Expiry Date"/>
                            </div>
                            <div class="justify-end pl-[100px]" >
                                <input bind:value={cardCvcState} type="text" class="input input-bordered w-full " placeholder="CVC Code"/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card w-full md:w-2/5 xl:w-2/5 bg-base-100 border-2 border-black-500 mt-8 ">
            <!-- New card content goes here -->
            <div class="card-body pl-20 pr-20 pt-10">
                <h1 class="card-title">Order Price</h1>
                <h1 class="card-title">Cart:<p style="text-align: right;">{(price).toFixed(2)}</p> </h1>
                <h1 class="card-title">Tax:<p style="text-align: right;">{(price * 0.0724776501).toFixed(2)}</p> </h1>
                <h1 class="card-title">Shipping:<p style="text-align: right;">{shipping}</p> </h1>
                <h1 class="card-title">Total:<p style="text-align: right;">{(shipping + (price * 0.0724776501) + price).toFixed(2)}</p> </h1>
                <button on:click={handlePaymentSubmit} class="btn bg-secondary mt-6">Pay Now</button>
            </div>
        </div>
    </div>
</html>

<style>
  /* Add your styles here */
</style>
