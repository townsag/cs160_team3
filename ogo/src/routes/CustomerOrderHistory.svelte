<script lang="ts">
    import { onMount } from "svelte";
    import OrderSummaryCustomer from "../lib/components/OrderSummaryCustomer.svelte";
    import Navbar from "../lib/components/Navbar.svelte";

    let username: string;
    let orders_props: any = [];

    async function get_username() {
        try {
            const username_response = await fetch("/getUser");
            if (username_response.ok) {
                const data = await username_response.json();
                username = data.username;
            }
        } catch (error) {
            console.log("error: ", error);
        }
    }

    async function get_order_info() {
        try {
            const orders_response = await fetch("/getOrders");
            console.log("this is orders responce: ", orders_response.ok);
            // console.log("this is the response", orders_response);
            // console.log(orders_response.json());
            if (orders_response.ok) {
                orders_props = await orders_response.json();
                console.log("this is the orders response: ", orders_props);
            } else {
                console.error("Failed to fetch data");
            }
            console.log("this is length of response: ", orders_props.length);
        } catch (error) {
            console.log("error: ", error);
        }
    }

    onMount(async () => {
        get_username();
        await get_order_info();
    });
</script>

<style>
    .midContainer {
        display: flex;
        flex-direction: column;
        min-height: 80vh;
    }
</style>

<div class="midContainer">
    <Navbar />
    <div class="p-2">
        <div class="text-xl font-medium ml-3 mt-3">Order History:</div>
        <div class="ml-3 mb-3">{username}</div>
        {#if orders_props.length > 0}
            {#each orders_props as props}
                <div class="p-2">
                    <OrderSummaryCustomer {...props} />
                </div>
            {/each}
        {:else}
            <div>No Orders Placed</div>
            <!-- <div>user may not be logged in</div> -->
        {/if}
    </div>
</div>
