<script lang="ts">
    import { onMount } from 'svelte';
    import { getCart } from "../lib/util/RequestController"
    import ItemDisplay from '../lib/components/ItemDisplay.svelte';

    const taxRate = 0.0725;

    let filteredItems: any[] = [];

    let totalWeight = 0;
    let totalCost = 0;

    let itemsSubtotal = 0;
    let shippingSubtotal = 0;
    let taxSubtotal = 0;

    function calculateTotalCost() {
        totalWeight = Object.values(filteredItems).reduce((acc, item) => acc + item.weight, 0);

        itemsSubtotal = Object.values(filteredItems).reduce((acc, item) => acc + item.price, 0);

        taxSubtotal = itemsSubtotal * taxRate;

        console.log("Total weight:", totalWeight);
        
        if (totalWeight > 20)
            shippingSubtotal = 20;
        else
            shippingSubtotal = 0;

        totalCost = itemsSubtotal + shippingSubtotal + taxSubtotal;
    }

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

    onMount(async () => {
        await handleGetCart();
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