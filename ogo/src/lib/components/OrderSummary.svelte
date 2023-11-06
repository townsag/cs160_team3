<script lang="ts">
    export let order_id: number;
    export let status: number; //0: placed, 1: in progress, 2: delivered
    export let placed_epoch: number;

    function epochToDate(epoch: number) {
        return new Date(epoch * 1000); // Multiply by 1000 to convert seconds to milliseconds
    }

    let order_date: Date = epochToDate(placed_epoch);

</script>

<div class="bg-green-500 h-1/6 w-full rounded-xl">
    <div class="flex flex-row place-content-around">
        <div class="text-md text-yellow-200 p-2">Order Number: {order_id}</div>
        <div class="text-sm text-yellow-200 p-2">Placed on: {order_date.getMonth()}/{order_date.getDay()}/{order_date.getFullYear()}</div>
    </div>
    <div class="flex justify-center p-2">
        <!-- <progress class="progress progress-secondary w-56" value={value} max="100"></progress> -->
        <progress class="progress w-5/6" value={100*(status+1)/3} max="100"></progress>
    </div>

</div>