<script lang="ts">
    import { onMount } from "svelte";
    import Map from "../lib/components/Map.svelte";
    import OrderSummaryEmployee from "../lib/components/OrderSummaryEmployee.svelte";
    import Navbar from "../lib/components/Navbar.svelte";
    import derp_bot from "../../public/derp-bot.png";
    import { alert } from "../lib/stores/alertStore";
    import AlertDaisy from "../lib/components/AlertDaisy.svelte";

    interface Order {
        order_id: number;
        status: number;
        placed_epoch: number;
        eta_epoch: number | null;
        total_price: number;
        total_weight: number;
        user: { [key: string]: string | number | boolean };
    }

    let route_data: any = {};
    let orders_props: Order[] = [];
    let routes_list: any = [];
    let username: string = "none";
    let API_KEY: string = "none";

    let routed_orders: any = [];
    let unrouted_orders: any = [];

    let returned_routes_flag = false;
    let returned_route_info = false;
    let map_init_flag = false;
    let selected_route: number = 1;

    let map_obj: any;

    async function get_all_routes() {
        try {
            const routes_list_response = await fetch("/getRoutesList");
            if (routes_list_response.ok) {
                interface RouteListItem {
                    route_id: string;
                    creation_epoch: number;
                }
                const data: RouteListItem[] = await routes_list_response.json();
                routes_list = data.map((item) => item.route_id);
                console.log(
                    "inside get all routes this is routes list: ",
                    routes_list
                );

                if (routes_list.length > 0) {
                    returned_routes_flag = true;
                    console.log("inside get all routes if block");
                    console.log(
                        "about to query routes list zero 0, route_id: ",
                        routes_list[0]
                    );
                    await get_route_info(routes_list[0]);
                    // console.log("this is the polyline: ", route_data.polyline);
                    //Todo: source of potential bug, will return error if async function gets here before
                    //      map object is initialized. Also cant call this function onMOunt because map
                    //      object wont exist
                    await map_obj.init_map();
                    map_init_flag = true;
                    await map_obj.add_polyline(route_data.polyline);
                    await map_obj.add_markers(route_data.legs);
                    console.log("LEGS!");
                    console.log(route_data.legs);

                    map_obj.startMovingMarker(
                        route_data.creation_epcoh,
                        route_data.end_epoch
                    );
                }
            }
        } catch (error) {
            console.log("error: ", error);
        }
    }

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

    async function get_api_key() {
        try {
            const api_key_response = await fetch("/getMapConstants");
            if (api_key_response.ok) {
                const data = await api_key_response.json();
                API_KEY = data.API_KEY;
            }
        } catch (error) {
            console.log("error: ", error);
        }
    }

    async function get_route_info(route_id: number) {
        try {
            // const route_id = 1;
            console.log("inside get route info with id: ", route_id);
            const map_response = await fetch(
                `/getRouteWithUsername?route_id=${route_id}`
            );
            if (map_response.ok) {
                route_data = await map_response.json();
                returned_route_info = true;
                console.log(route_data);
            } else {
                console.log("error reaching get route endpoint");
                console.log(map_response.statusText);
            }
        } catch (error) {
            console.log("error: ", error);
        }
    }

    async function get_all_order_info() {
        try {
            const all_orders_response = await fetch("/getAllOrders");
            console.log("this is orders responce: ", all_orders_response.ok);
            console.log("this is the response", all_orders_response);
            if (all_orders_response.ok) {
                orders_props = await all_orders_response.json();
                console.log("This is all orders: ", orders_props);

                routed_orders = [];
                unrouted_orders = [];

                orders_props.forEach(order => {
                    if (order.status > 0){
                        routed_orders.push(order);
                    } else {
                        unrouted_orders.push(order);
                    }
                });
            } else {
                console.error("Failed to fetch data");
            }
            console.log("this is length of response: ", orders_props.length);
        } catch (error) {
            console.log("error: ", error);
        }
    }

    async function handleSelect(event: Event) {
        const target = event.target as HTMLSelectElement;
        selected_route = Number(target.value);
        await get_route_info(selected_route);
        if (map_init_flag) {
            map_obj.add_polyline(route_data.polyline);
            map_obj.add_markers(route_data.legs);
            map_obj.startMovingMarker(
                route_data.creation_epcoh,
                route_data.end_epoch
            );
        }
    }
    //hardcoded values rn:
    //  -center of map (in map component)

    async function force_route() {
        const resp = await fetch("/forceRouteCreation");

        if (!resp.ok) {
            console.log("Routing Failed!");
            alert.set({
                show: true,
                message: "Routing failed. No queued orders to route.",
                type: "error",
            });
            return;
        }

        alert.set({
            show: true,
            message: "Orders routed successfully.",
            type: "success",
        });
        get_all_routes();
        get_all_order_info();
    }

    get_username();
    get_api_key();
    get_all_routes();
    get_all_order_info();
</script>

<!-- svelte-ignore a11y-missing-attribute -->
<Navbar />
<AlertDaisy {alert} />
<div class="flex flex-row justify-between items-center">
    <div class="p-5 text-xl">Welcome to employee home: {username}</div>
    {#if returned_routes_flag}
        <div class="">
            <select
                class="select select-sm select-bordered text-lg font-normal mt-1"
                on:change={handleSelect}
            >
                {#each routes_list as option}
                    <option value={option}>Route ID: {String(option)}</option>
                {/each}
            </select>
            <div
                class="tooltip tooltip-bottom tooltip-primary"
                data-tip="Bypass AutoRouter"
            >
                <button on:click={force_route} class="btn btn-sm mx-4"
                    >Force Route</button
                >
            </div>
        </div>
    {/if}
</div>
{#if !returned_routes_flag}
    <div class="flex flex-col items-center">
        <img
            alt="delivery robot"
            src={derp_bot}
            class="max-h-80 object-scale-down"
        />
        <div class="text-md">
            OgO bot is ready to deliver orders, routes will display when
            products are ordered"
        </div>
    </div>
{/if}
<div>
    {#if returned_routes_flag && returned_route_info && API_KEY !== "none"}
        <!-- <p>route id: {route_data.route_id}</p>
        <p>route legs: {route_data.legs}</p> -->
        <Map bind:this={map_obj} {API_KEY} />
        <!-- {:else}
        <p>map component not rendered because missing props</p>
        <p>{route_data}</p>
        <p>{API_KEY}</p> -->
    {/if}
</div>

<div class="p-2">
    {#if orders_props.length > 0}
        <div class="flex flex-col">
            {#if unrouted_orders.length > 0}
                <div class="text-2xl ml-2">Unrouted Orders:</div>
            {/if}
            {#each unrouted_orders as props (props.order_id)}
                <div class="p-2">
                    <OrderSummaryEmployee {...props} />
                </div>
            {/each}
            {#if routed_orders.length > 0}
                <div class="text-2xl ml-2">Routed Orders:</div>
            {/if}
            {#each routed_orders as props (props.order_id)}
                <div class="p-2">
                    <OrderSummaryEmployee {...props} />
                </div>
            {/each}
        </div>
    {:else}
        <p>This user may not have placed orders yet</p>
        <p>Or this user may not be authenticated as an admin</p>
    {/if}
</div>


