<script lang="ts">
    import { onMount } from "svelte";

    import OrderTable from "./OrderTable.svelte";

    export let order_id: number;
    export let status: number; //0: placed, 1: in progress, 2: delivered
    export let placed_epoch: number;
    export let eta_epoch: number;
    export let total_price: number;
    export let total_weight: number;

    function epochToDate(epoch: number) {
        return new Date(epoch * 1000); // Multiply by 1000 to convert seconds to milliseconds
    }

    let order_date: Date = epochToDate(placed_epoch);
    let eta_date: Date = epochToDate(eta_epoch);
    let order_product_info: any[] = [];

    async function get_order_products() {
        try {
            const order_products_response = await fetch(
                `/getOrderItems?orderID=${order_id}`
            );
            if (order_products_response.ok) {
                order_product_info = await order_products_response.json();
                console.log("order products response: ", order_product_info);
            } else {
                console.log("error reaching get order items endpoint");
                console.log(order_products_response.statusText);
            }
        } catch (error) {
            console.log("error: ", error);
        }
    }
    onMount(async () => {
        await get_order_products();
    });
</script>

<details class="collapse collapse-arrow border">
    <summary class="collapse-title">
        <div class="flex flex-row place-content-around">
            <div class="text-xl font-medium">Order #{order_id}</div>
            <div>
                {order_date.getMonth()}/{order_date.getDay()}/{order_date.getFullYear()}
            </div>
            <div>${total_price.toFixed(2)}</div>
        </div>
        <div class="flex flex-row place-content-around mt-2">
            <progress
                class="progress w-5/6"
                value={(100 * (status + 1)) / 3}
                max="100"
            />
        </div>
    </summary>
    <div class="collapse-content">
        {#if eta_epoch != null}
            <div class="p-2">
                ETA: {eta_date.getMonth()}/{eta_date.getDay()}/{eta_date.getFullYear()}
            </div>
        {:else}
            <div class="p-2">ETA: pending</div>
        {/if}
        <OrderTable {order_id} />
    </div>
</details>
