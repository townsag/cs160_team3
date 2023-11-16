<script lang="ts">
  import { onMount } from "svelte";

  import OrderTable from "./OrderTable.svelte";

  export let order_id: number;
  export let status: number; //0: placed, 1: in progress, 2: delivered
  export let placed_epoch: number;
  export let eta_epoch: number | null;
  export let total_price: number;
  export let total_weight: number;
  export let user: { [key: string]: string | boolean | number };

  let extend_flag: Boolean = false;
  let button_text: string = "see more";

  function epochToDate(epoch: number) {
    let d = new Date(epoch * 1000); // Multiply by 1000 to convert seconds to milliseconds
    return `${d.getFullYear()}/${d.getMonth() + 1}/${d.getDay()} ${
      d.getHours() % 12 || 12
    }:${d.getMinutes().toString().padStart(2, "0")} ${
      d.getHours() >= 12 ? "PM" : "AM"
    }`;
  }

  let order_date: string = epochToDate(placed_epoch);
  let eta_date: string = "pending...";
  if (eta_epoch != null) {
    eta_date = epochToDate(eta_epoch);
  }

  let order_product_info: any = [];

  async function get_order_products() {
    try {
      const order_products_response = await fetch(
        `/getOrderItemsEmployee?userID=${user.user_id}&orderID=${order_id}`
      );

      if (order_products_response.ok) {
        order_product_info = await order_products_response.json();
        console.log("order products response: ", order_product_info);
      } else {
        console.log(
          "error reaching get order items endpoint, maybe user is not admin"
        );
        console.log(order_products_response.statusText);
      }
    } catch (error) {
      console.log("error: ", error);
    }
  }
  onMount(async () => {
    console.log("in on mount for order summary employee id: ", order_id);
    await get_order_products();
  });
</script>

<details class="collapse collapse-arrow border shadow-md">
  <summary class="collapse-title">
    <div class="flex flex-row place-content-around">
      <div class="text-xl font-medium p-2">Order #{order_id}</div>
      <div class="text-md p-2">
        Placed on: {order_date}
      </div>
      <div class="text-md p-2">Username: {user.username}</div>
      <!-- <div>${total_price.toFixed(2)}</div> -->
    </div>
    <div class="flex flex-row place-content-around mt-2">
      <progress
        class="progress progress-primary w-5/6"
        value={(100 * (status + 1)) / 3}
        max="100"
      />
    </div>
  </summary>
  <div class="collapse-content">
    <div class="flex flex-row justify-evenly m-2">
      <div class="text-md p-2">Price: ${total_price.toFixed(2)}</div>
      <div class="text-md p-2">Weight: {total_weight.toFixed(2)} lbs</div>
      <div class="p-2">
        ETA: {eta_date}
      </div>
    </div>
    <OrderTable {order_id} />
  </div>
</details>
