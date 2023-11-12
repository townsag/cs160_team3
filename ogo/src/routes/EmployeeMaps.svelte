
<script lang="ts">
    import Map from "../lib/components/Map.svelte";
    import RouteSummary from "../lib/components/RouteSummary.svelte";
    import Navbar from "../lib/components/Navbar.svelte";

    let route_data: any = {};
    let orders_props: any = [];
    let username: string = "none";
    let API_KEY: string = "none";

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
    
    // async function get_api_key() {
    //     try{
    //         const api_key_response = await fetch("/getMapConstants");
    //         if(api_key_response.ok){
    //             const data = await api_key_response.json();
    //             API_KEY = data.API_KEY;
    //         }
    //     } catch (error) {
    //         console.log("error: ", error)
    //     }
    // }
    //hardcoded values rn:
    //  -API key
    //  -route id
    //  -center of map (in map component)

    

    async function sequential_api_calls(){
        const route_id = 1;

        
        try{
            const api_key_response = await fetch("/getMapConstants");
            // console.log(api_key_response.text());
            if(api_key_response.ok){
                const data = await api_key_response.json();
                API_KEY = data.API_KEY;
                console.log("api key: ", API_KEY);
            } else {
                console.log("failed to reach map constants api");
            }
        } catch (error) {
            console.log("error: ", error);
        }

        try{
            const map_response = await fetch(`/getRoute?route_id=${route_id}`);
            if (map_response.ok){
                route_data = await map_response.json();
                console.log(route_data);
            } else {
                console.log("error reaching get route endpoint");
                console.log(map_response.statusText);
            }

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
    }
    
    get_username();
    sequential_api_calls();

    console.log("api key: ", API_KEY, "maps data: ", route_data);
    /*
    async function get_map(){
        const route_id = 1;
        const api_key = "asdf";
        try{
            const map_response = await fetch(`/getRoute?route_id=${route_id}`);
            if (map_response.ok){
                route_data = await map_response.json();
                console.log(route_data);
            } else {
                console.log("error reaching get route endpoint");
                console.log(map_response.statusText);
            }
        } catch (error){
            console.log("error: ", error);
        }
    }

    async function get_orders(){
        try {
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
        } catch (error) {
            console.log("error: ", error);
        }
    }
    
    get_username();
    console.log("calling get map");
    get_map();*/

    // console.log("calling get orders");
    // get_orders();

    // const orders_list =[
	// 	{
	// 		order_number: 12345,
	// 		order_status: 0,
	// 		order_date: new Date(1999, 3, 15),
	// 	},
	// 	{
	// 		order_number: 45678,
	// 		order_status: 1,
	// 		order_date: new Date(1999, 3, 13),
	// 	},
	// 	{
	// 		order_number: 56789,
	// 		order_status: 2,
	// 		order_date: new Date(1999, 3, 12),
	// 	}
	// ];
</script>


<!-- svelte-ignore a11y-missing-attribute -->
<html>
    <body>
        <Navbar/>
        <h1>Welcome to employee home: {username}</h1>
        <div>
            <div>
                {#if Object.keys({route_data}).length > 0 && API_KEY !== "none"}
                    <Map API_KEY={API_KEY} map_data={route_data}/>
                {:else}
                    <p>map component not rendered because missing props</p>
                {/if}
            </div>
            <div class="p-2 bg-yellow-200">
                {#if orders_props.length > 0}
                    {#each orders_props as props (props.order_id)}
                        <div class="p-2">
                            <RouteSummary {...props} />
                        </div>
                    {/each}
                {:else}
                        <p>This user may not have placed orders yet</p>
                {/if}
            </div>
        </div>
    </body>
</html>

<!-- <style>
    .map-holder {
        width: 100%;
        height: 100%;
        border-radius: 25px;
    }
</style> -->