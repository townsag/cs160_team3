<script lang="ts">
  import { onMount } from "svelte";

  export let order_id: number;

  let products_list: any[] = [];

  async function fetch_order_products() {
    try {
      const order_products_response = await fetch(
        `/getOrderItems?orderID=${order_id}`
      );
      if (order_products_response.ok) {
        products_list = await order_products_response.json();
        console.log("order products response: ", products_list);
      } else {
        console.log("error reaching get order items endpoint");
        console.log(order_products_response.statusText);
      }
    } catch (error) {
      console.log("error: ", error);
    }
  }

  onMount(async () => {
    await fetch_order_products();
  });
</script>

<div>
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
        {#each products_list as p}
          <tr class="hover">
            <td>
              <div class="flex items-center gap-3 m-0">
                <div class="avatar">
                  <div class="mask w-12 h-12">
                    <img src={p.image} alt="Product Image" />
                  </div>
                </div>
              </div>
            </td>
            <td>
              <a class="font-bold" href="/itemView/{p.product_id}">{p.name}</a>
            </td>
            <td>{p.quantity}</td>
            <td>{p.price * p.quantity}$</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>
