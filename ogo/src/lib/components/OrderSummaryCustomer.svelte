<script lang="ts">
  import { onMount } from "svelte";

    export let order_id: number;
    export let status: number; //0: placed, 1: in progress, 2: delivered
    export let placed_epoch: number;
    export let eta_epoch: number;
    export let total_price: number;
    export let total_weight: number;

    let extend_flag: Boolean = false;
    let button_text: string = "see more";
    function onClick() {
        extend_flag = !extend_flag
        if (extend_flag){
            button_text = "see less";
        } else {
            button_text = "see more";
        }
    }

    function epochToDate(epoch: number) {
        return new Date(epoch * 1000); // Multiply by 1000 to convert seconds to milliseconds
    }

    let order_date: Date = epochToDate(placed_epoch);
    let eta_date: Date = epochToDate(eta_epoch);
    let order_product_info: any = []

    async function get_order_products(){
        try {
            const order_products_response = await fetch(`/getOrderItems?orderID=${order_id}`);
            if (order_products_response.ok){
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
    onMount(async () =>{
        await get_order_products();
    })


</script>

<div class="bg-green-500 h-1/6 w-full rounded-xl">
    <div class="flex flex-row place-content-around">
        <div class="text-md text-yellow-200 p-2">Order num: {order_id}</div>
        <div class="text-md text-yellow-200 p-2">Placed on: {order_date.getMonth()}/{order_date.getDay()}/{order_date.getFullYear()}</div>
        <button class="bg-yellow-200 rounded-lg w-1/6 p-1 m-2" on:click={onClick}>{button_text}</button>
    </div>
    <div class="flex justify-center p-2">
        <!-- <progress class="progress progress-secondary w-56" value={value} max="100"></progress> -->
        <progress class="progress w-5/6" value={100*(status+1)/3} max="100"></progress>
    </div>
    {#if extend_flag}
        <div class="flex flex-row justify-evenly">
            <div class="text-md text-yellow-200 p-2">order price: {total_price}</div>
            <div class="text-md text-yellow-200 p-2">order weight: {total_weight}</div>
            {#if eta_epoch != null}
                <div class="text-md text-yellow-200 p-2">ETA: {eta_date.getMonth()}/{eta_date.getDay()}/{eta_date.getFullYear()}</div>
            {:else}
                <div class="text-md text-yellow-200 p-2">ETA: pending</div>
            {/if}
        </div>
        {#if (order_product_info.length > 0)}
            <div class="flex flex-col justify-evenly p-2">
                {#each order_product_info as product}
                    <div class="flex flex-row justify-evenly bg-yellow-200 rounded-xl m-2">
                        <div class="text-md p-2">Product Name: {product.name}</div>
                        <div class="text-md p-2">Product quantity: {product.quantity}</div>
                    </div>
                {/each}
            </div>
        {/if}
    {/if}

</div>