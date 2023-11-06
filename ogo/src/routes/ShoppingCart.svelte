<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { getCart } from "../lib/util/RequestController"
    import { cartItemQuantitySignal, cartItemRemovedSignal } from "../lib/stores/CartObserver";
    import ItemDisplay from "../lib/components/ItemDisplay.svelte";

    // California sales tax rate
    const TAX_RATE = 0.0725;

    let filteredItems: any[] = [];

    let totalWeight = 0;
    let totalCost = 0;

    let itemsSubtotal = 0;
    let shippingSubtotal = 0;
    let taxSubtotal = 0;

    // calculate total cost of the order for itemized summary purposes
    function calculateTotalCost() {
        totalWeight = Object.values(filteredItems).reduce((acc, item) => acc + (item.weight * item.quantity), 0);
        itemsSubtotal = Object.values(filteredItems).reduce((acc, item) => acc + (item.price * item.quantity), 0);
        taxSubtotal = itemsSubtotal * TAX_RATE;

        console.log("Total weight:", totalWeight);
        
        if (totalWeight > 20)
            shippingSubtotal = 20;
        else
            shippingSubtotal = 0;

        totalCost = itemsSubtotal + shippingSubtotal + taxSubtotal;
    }

    // retrieve cart data
    async function handleGetCart() {
        const result = await getCart();

        if (result.success) {
            //console.log(JSON.stringify(result));

            filteredItems = result.cart.items
            calculateTotalCost();
        } else {
            console.error("Failed to fetch cart data:", result.message);
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

<html lang="en" data-theme="lemonade">
    <div class="flex flex-row">
        <div class="basis-1/2">
            <div class="card bg-base-100 border-2 border-black-500 mt-8 mb-8">
                <div class="card-body">
                    <h1 class="card-title mb-8">ORDER SUMMARY</h1>

                    <div class="grid grid-rows-4 grid-flow-col gap-4">

                        {#if filteredItems && filteredItems.length > 0}
                            <ItemDisplay
                                {filteredItems}
                                isCartItem={true}
                            />
                        {:else}
                            <span>There are no items in your cart.</span>
                        {/if}

                        <!--test placeholder-->
                        <!-- {#each filteredItems as item}
                            <div class="card bg-neutral text-neutral-content">
                                <div class="card-body items-center text-center">
                                    <h2 class="card-title">{item.name}</h2>
                                </div>
                            </div>
                        {/each} -->

                    </div>
                </div>
            </div>
        </div>
        <div class="basis-1/2">
            <div class="card bg-base-100 border-2 border-black-500 mt-8 mb-8">
                <div class="card-body">
                    <h1 class="card-title mb-8">ORDER PRICE</h1>

                    <div class="flex flex-row">

                        <div class="basis-1/2">
                            <p class="text-center">Item(s) Subtotal</p>
                            <p class="text-center">Shipping Costs</p>
                            <p class="text-center">Taxes</p>
                            <p class="text-center">Total Cost</p>
                        </div>

                        <div class="basis-1/2">
                            <p class="text-center">${itemsSubtotal.toFixed(2)}</p>
                            <p class="text-center">${shippingSubtotal.toFixed(2)}</p>
                            <p class="text-center">${taxSubtotal.toFixed(2)}</p>
                            <p class="text-center">${totalCost.toFixed(2)}</p>
                        </div>

                    </div>

                    <progress class="progress progress-primary mt-16" value={Math.min((totalWeight / 20) * 100, 100)} max="100"></progress>

                    <p class="text-center">
                        {#if (totalWeight > 20)}
                            You are NOT QUALIFIED for FREE shipping.   
                        {:else}
                            You are QUALIFIED for FREE shipping.
                        {/if}
                    </p>

                    <div class="flex justify-center">
                        <button class="btn btn-secondary mt-16">Proceed to Payment</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</html>

<style>

</style>