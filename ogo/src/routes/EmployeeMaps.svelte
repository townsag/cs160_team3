
<script lang="ts">
  import { onMount } from "svelte";
    import Map from "../lib/components/Map.svelte";
    // import OrderSummaryCustomer from "../lib/components/OrderSummaryCustomer.svelte";
    // import Dropdown from "../lib/components/Dropdown.svelte";
    import OrderSummaryEmployee from "../lib/components/OrderSummaryEmployee.svelte";

    let route_data: any = {};
    let orders_props: any = [];
    let routes_list: any = [];
    let username: string = "none";
    let API_KEY: string = "none";

    let returned_routes_flag = false;
    let returned_route_info = false;
    let map_init_flag = false;
    let selected_route: number = 1;

    let map_obj: any;

    async function get_all_routes() {
        try{
            const routes_list_response = await fetch("/getRoutesList");
            if(routes_list_response.ok){
                interface RouteListItem {
                    route_id: string;
                    creation_epoch: number;
                }
                const data: RouteListItem[] = await routes_list_response.json();
                routes_list = data.map(item => item.route_id);
                console.log("inside get all routes this is routes list: ", routes_list);

                if (routes_list.length > 0){
                    returned_routes_flag = true;
                    console.log("inside get all routes if block");
                    console.log("about to query routes list zero 0, route_id: ", routes_list[0]);
                    await get_route_info(routes_list[0]);
                    // console.log("this is the polyline: ", route_data.polyline);
                    //Todo: source of potential bug, will return error if async function gets here before
                    //      map object is initialized. Also cant call this function onMOunt because map
                    //      object wont exist
                    await map_obj.init_map();
                    map_init_flag = true;
                    await map_obj.add_polyline(route_data.polyline);
                    await map_obj.add_markers(route_data.legs);

                }
            }
        } catch (error) {
            console.log("error: ", error);
        }
        
    }

    async function get_username(){
        try{
            const username_response = await fetch("/getUser");
            if(username_response.ok){
                const data = await username_response.json();
                username = data.username;
            }
        } catch (error){
            console.log("error: ", error);
        }
    }
    
    async function get_api_key() {
        try{
            const api_key_response = await fetch("/getMapConstants");
            if(api_key_response.ok){
                const data = await api_key_response.json();
                API_KEY = data.API_KEY;
            }
        } catch (error) {
            console.log("error: ", error)
        }
    }

    async function get_route_info(route_id: number){
        try{
            // const route_id = 1;
            console.log("inside get route info with id: ", route_id);
            const map_response = await fetch(`/getRoute?route_id=${route_id}`);
            if (map_response.ok){
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

    /*
    =====Depricated=====
    async function get_order_info(){
        try{
            const orders_response = await fetch("/getOrders");
            console.log("this is orders responce: ", orders_response.ok);
            console.log("this is the response", orders_response);
            // console.log(orders_response.json());
            if (orders_response.ok){
                orders_props = await orders_response.json();
            } else {
                console.error('Failed to fetch data');
            }
            console.log("this is length of response: ", orders_props.length);
        } catch (error){
            console.log("error: ", error);
        }
    }*/

    async function get_all_order_info(){
        try{
            const all_orders_response = await fetch("/getAllOrders");
            console.log("this is orders responce: ", all_orders_response.ok);
            console.log("this is the response", all_orders_response);
            if (all_orders_response.ok){
                orders_props = await all_orders_response.json();
            } else {
                console.error('Failed to fetch data');
            }
            console.log("this is length of response: ", orders_props.length);
        } catch (error){
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
        }
        
    }
    //hardcoded values rn:
    //  -center of map (in map component)
    
    //=====uncomment this=====//
    // onMount(async ()=>{
    //     get_username();
    //     await get_api_key();
    //     get_all_routes();
    //     get_all_order_info();
    // })
    get_username();
    get_api_key();
    get_all_routes();
    get_all_order_info();
    
    
    
    // get_order_info();
    
    
</script>

<!-- svelte-ignore a11y-missing-attribute -->
<div class="bg-green-500 flex flex-row justify-around items-center">
    <div class="p-5 text-yellow-200 text-xl">Welcome to employee home: {username}</div>
    {#if returned_routes_flag}
        <div class="bg-green-500">
            <select on:change={handleSelect} class="bg-yellow-200 text-md rounded-lg p-2 m-2">
                {#each routes_list as option}
                    <option value={option}>Route_id: {String(option)}</option>
                {/each}
            </select>
        </div>
    {:else}
        <!-- TODO: Add a more descriptive error message, have 
            no routes been made yet or was there a network error -->
        <p>dropdown not rendering because no routes</p>
    {/if}
</div>
<div>
    {#if returned_routes_flag && returned_route_info && API_KEY !== "none"}
        <!-- <p>route id: {route_data.route_id}</p>
        <p>route legs: {route_data.legs}</p> -->
        <Map bind:this={map_obj} API_KEY={API_KEY}/>
    {:else}
        <p>map component not rendered because missing props</p>
        <p>{route_data}</p>
        <p>{API_KEY}</p>
    {/if}
</div>


<!-- <h1>Welcome to employee home: {username}</h1>
<div>
    {#if returned_routes_flag}
        
        <div class="bg-green-500">
            <select on:change={handleSelect} class="bg-yellow-200 text-md rounded-lg  w-1/6 p-2 m-2">
                {#each routes_list as option}
                    <option value={option}>Route_id: {String(option)}</option>
                {/each}
            </select>
        </div>
        
        {#if returned_route_info && API_KEY !== "none"}
            
            <Map bind:this={map_obj} API_KEY={API_KEY}/>
        {:else}
            <p>map component not rendered because missing props</p>
            <p>{route_data}</p>
            <p>{API_KEY}</p>
        {/if}
    {:else}
        <p>dropdown and map missing because failed to recieve routes list</p>
    {/if}
</div> -->
<div class="p-2 bg-yellow-200">
    {#if orders_props.length > 0}
        {#each orders_props as props (props.order_id)}
            <div class="p-2">
                <OrderSummaryEmployee {...props} />
            </div>
        {/each}
    {:else}
            <p>This user may not have placed orders yet</p>
            <p>Or this user may not be authenticated as an admin</p>
    {/if}
</div>



<!-- <style>
    .map-holder {
        width: 100%;
        height: 100%;
        border-radius: 25px;
    }
</style> -->



