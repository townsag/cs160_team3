<script lang="ts">
  import { onMount } from "svelte";

    export let order_id: number;
    export let status: number; //0: placed, 1: in progress, 2: delivered
    export let placed_epoch: number;
    export let eta_epoch: number | null;
    export let total_price: number;
    export let total_weight: number;
    export let user: {[key: string]: string | boolean | number};

    let extend_flag: Boolean = false;
    let button_text: string = "see more";
    // function onClick() {
    //     extend_flag = !extend_flag
    //     if (extend_flag){
    //         button_text = "see less";
    //     } else {
    //         button_text = "see more";
    //     }
    // }

    function epochToDate(epoch: number) {
        return new Date(epoch * 1000); // Multiply by 1000 to convert seconds to milliseconds
    }

    let order_date: Date = epochToDate(placed_epoch);
    let eta_date: Date;
    if (eta_epoch != null){
        eta_date = epochToDate(eta_epoch);
    }

    let order_product_info: any = []

    async function get_order_products(){
        try {
            const order_products_response = await fetch(`/getOrderItemsEmployee?userID=${user.user_id}&orderID=${order_id}`);

            if (order_products_response.ok){
                order_product_info = await order_products_response.json();
                console.log("order products response: ", order_product_info);
            } else {
                console.log("error reaching get order items endpoint, maybe user is not admin");
                console.log(order_products_response.statusText);
            }
        } catch (error) {
            console.log("error: ", error);
        }
    }
    onMount(async () =>{
        console.log("in on mount for order summary employee id: ", order_id);
        await get_order_products();
    })

</script>


<details class="collapse collapse-arrow border shadow-md">
    <summary class="collapse-title">
        <div class="flex flex-row place-content-around">
            <div class="text-xl font-medium p-2">Order #{order_id}</div>
            <div class="text-md p-2">
                Placed on: {order_date.getMonth()}/{order_date.getDay()}/{order_date.getFullYear()}
            </div>
            <div class="text-md p-2">Username: {user.username}</div>
            <!-- <div>${total_price.toFixed(2)}</div> -->
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
        <div class="flex flex-row justify-evenly m-2">
            <div class="text-md p-2">Price: {total_price}</div>
            <div class="text-md p-2">Weight: {total_weight}</div>
            {#if eta_epoch != null}
                <div class="p-2">
                    ETA: {eta_date.getMonth()}/{eta_date.getDay()}/{eta_date.getFullYear()}
                </div>
            {:else}
                <div class="p-2">ETA: pending</div>
            {/if}

        </div>
        <div class="overflow-x-auto">
            <table class="table table-sm">
              <thead>
                <tr>
                  <th />
                  <th>Product</th>
                  <th>Quantity</th>
                  <th>Price</th>
                </tr>
              </thead>
              <tbody>
                {#each order_product_info as p}
                  <tr class="hover">
                    <td class="p-0">
                      <div class="flex items-center gap-3 m-0">
                        <div class="avatar">
                          <div class="mask w-12 h-12">
                            <img src={p.image} alt="Product in order" />
                          </div>
                        </div>
                      </div>
                    </td>
                    <td>
                      <a class="font-bold" href="/itemView/{p.product_id}">{p.name}</a>
                    </td>
                    <td>{p.quantity}</td>
                    <td>${(p.price * p.quantity).toFixed(2)}</td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
    </div>
</details>