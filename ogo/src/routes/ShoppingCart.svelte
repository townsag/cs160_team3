<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { getCart } from "../lib/util/RequestController"
    import { cartItemQuantitySignal, cartItemRemovedSignal } from "../lib/stores/CartObserver";
    import ItemDisplay from "../lib/components/ItemDisplay.svelte";
    import { navigate } from "svelte-routing";
    import Navbar from "../lib/components/Navbar.svelte";

    import { alert } from '../lib/stores/alertStore';
    import AlertDaisy from "../lib/components/AlertDaisy.svelte";

    // California sales tax rate
    const TAX_RATE = 0.0725;
    const SHIPPING_COST = 10;
    const MAX_SHIPPING_COST_WEIGHT = 20;
    const MAX_CART_WEIGHT = 200;

    let filteredItems: any[] = [];

    let totalWeight = 0;
    let totalCost = 0;

    let itemsSubtotal = 0;
    let shippingSubtotal = 0;
    let taxSubtotal = 0;

    let paymentDisabledState = true;

    // calculate total cost of the order for itemized summary purposes
    function calculateTotalCost() {
        totalWeight = Object.values(filteredItems).reduce((acc, item) => acc + (item.weight * item.quantity), 0);
        itemsSubtotal = Object.values(filteredItems).reduce((acc, item) => acc + (item.price * item.quantity), 0);
        taxSubtotal = itemsSubtotal * TAX_RATE;
        console.log("Total weight:", totalWeight);
        if (totalWeight > MAX_SHIPPING_COST_WEIGHT)
            shippingSubtotal = SHIPPING_COST;
        else
            shippingSubtotal = 0;
        totalCost = itemsSubtotal + shippingSubtotal + taxSubtotal;
    }

    // retrieve cart data
    async function handleGetCart() {
        const result = await getCart();

        if (result.success) {
            filteredItems = result.cart.items
            console.log(filteredItems);

            // disable payment button if cart is empty
            if (filteredItems.length !== 0) {
                paymentDisabledState = false;
            } else {
                paymentDisabledState = true;
            }
            calculateTotalCost();
        } else {
            console.error("Failed to fetch cart data:", result.message);
        }
    }

    $: {
        if (totalWeight > MAX_CART_WEIGHT || filteredItems.length == 0) {
            paymentDisabledState = true;
        } else {
            paymentDisabledState = false;
        }
    }

    // get cart onMount
    onMount(async () => {
        await handleGetCart();
    });

    // signals for cart changes to make the page reactive
    const quantitySignalUnsubscribe = cartItemQuantitySignal.subscribe(() => {
        handleGetCart();
    })

    const removedSignalUnsubscribe = cartItemRemovedSignal.subscribe(() => {
        handleGetCart();
    })

    // unsubscribe from signals to prevent memory leaks when component is not in use
    onDestroy(() => {
        quantitySignalUnsubscribe();
        removedSignalUnsubscribe();
    });
</script>

<style>
    .midContainer {
        display: flex;
        flex-direction: column-reverse;
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
            <div class="card bg-base-100 border-2 border-black-500 m-8 mt-4 lg:mt-8 lg:mr-4 shadow-md" >
                <div class="card-body">
                    <h1 class="card-title mb-4">ORDER SUMMARY</h1>
                    {#if filteredItems && filteredItems.length > 0}
                        <ItemDisplay
                            {filteredItems}
                            isAdmin={false}
                            isCartItem={true}
                        />
                    {:else}
                        <span>There are no items in your cart.</span>
                    {/if}
                </div>
            </div>
        </div>
        <div class="basis-1/2">
            <div class="card bg-base-100 border-2 border-black-500 m-8 mb-4 lg:mb-8 lg:ml-4 shadow-md">
                <div class="card-body">
                    <h1 class="card-title mb-4">ORDER PRICE</h1>

                    <div class="flex flex-row">
                        <div class="basis-1/2">
                            <p class="text-left"><b>Item(s) Subtotal:</b></p>
                            <p class="text-left"><b>Shipping Costs:</b></p>
                            <p class="text-left"><b>Taxes:</b></p>
                            <p class="text-left"><b>Total Cost:</b></p>
                            <div class="divider"></div> 
                            <p class="text-left"><b>Total Weight:</b></p>
                        </div>

                        <div class="basis-1/2">
                            <p class="text-right">${itemsSubtotal.toFixed(2)}</p>
                            <p class="text-right">${shippingSubtotal.toFixed(2)}</p>
                            <p class="text-right">${taxSubtotal.toFixed(2)}</p>
                            <p class="text-right">${totalCost.toFixed(2)}</p>
                            <div class="divider"></div> 
                            <p class="text-right">{totalWeight.toFixed(2)} lb.</p>
                        </div>
                    </div>

                    <progress class="progress progress-primary mt-16" value={Math.min((totalWeight / 20) * 100, 100)} max="100"></progress>

                    <p class="text-center">({totalWeight.toFixed(2)} lb. / 20.00 lb.)</p>

                    <p class="text-center">
                        {#if (totalWeight > 20)}
                            You are NOT QUALIFIED for FREE shipping.<br>
                            Total weight must be less than 20 lb. to qualify for free shipping.
                        {:else if (totalWeight === 0)}
                            Add items to your cart.
                        {:else}
                            You are QUALIFIED for FREE shipping.
                        {/if}
                    </p>

                    <div class="flex justify-center w-full">
                        <button on:click={() => navigate('/payment')} class="btn btn-secondary w-full mt-16" disabled={paymentDisabledState}>
                            {#if (paymentDisabledState)}
                                {#if filteredItems.length == 0}
                                    Cart is Empty
                                {:else}
                                    Order is over 200lbs
                                {/if}
                            {:else}
                                Proceed to Payment
                            {/if}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</html>