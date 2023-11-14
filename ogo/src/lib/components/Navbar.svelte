<script lang="ts">
	import ogo from "../../assets/ogo.png";
	import logo from "../../assets/logo_icon.png";
	import { logout, getCart } from "../util/RequestController"
	import { cartItemQuantitySignal, cartItemRemovedSignal } from "../stores/CartObserver";
	import { navigate } from 'svelte-routing';
	import { onMount, onDestroy } from 'svelte';

	/* to use on other pgs u must have
		// in script
			import Navbar from "../lib/components/Navbar.svelte";
		// in html/body
			<Navbar/>
	*/

	let numCartItemsState = 0;

	async function handleLogout() {
		const result = await logout();

		if (result.success) {
			console.log("Logged out successfully!");
			userType = 0;
			navigate("/login");
		} else {
			console.error("Logout failed:", result.message);
		}
	}

	// retrieve cart data
	async function handleGetCart() {
        const result = await getCart();

        if (result.success) {
			numCartItemsState = Object.values(result.cart.items).reduce((acc: number, item: any) => acc + (item.quantity), 0);
        } else {
            console.error("Failed to fetch cart data:", result.message);
        }
    }

	function handleSettings() {
		navigate("/settings");
	}

	function handleShoppingCart() {
		navigate("/cart");
	}

	function handleMap() {
		navigate("/employeesmaps");
	}
	
	function handleOrders() {
		navigate("/customer-order-history");
	}

	function handleBrowse() {
		navigate("/browse");
	}

	let currentUser;
	// 0-not login, 1-user, 2-admin
	let userType = 0;
	async function sequential_api_calls(){
		try{                                  //getUser
			const response = await fetch("/getUser", { method: "GET" });
			const data = await response.json();
			currentUser = data;
			if (currentUser.is_admin) {
				userType = 2;
			} else {
				userType = 1;
			}
		} catch (error) {
			console.log("error: ", error);
			userType = 0;
			navigate("/login");
		}
	}

	onMount(async () => {
        sequential_api_calls();
		await handleGetCart();
    });

	// signals for cart changes to make the page reactive
	const quantitySignalUnsubscribe = cartItemQuantitySignal.subscribe(() => {
        handleGetCart();
    })

    const removedSignalUnsubscribe = cartItemRemovedSignal.subscribe(() => {
        handleGetCart();
    })

    // unsubscribe from signals to prevent memory leaks when component is not in use
    onDestroy(() => {
        quantitySignalUnsubscribe();
        removedSignalUnsubscribe();
    });
</script>

<style>
	.navbar {
		box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Adjust the values as needed */
	}
</style>

{#if userType > 0}
	<div class="navbar px-4">
		<div class="flex-1">
			<a class="btn btn-ghost normal-case text-xl" href="/browse">
				<!-- svelte-ignore a11y-missing-attribute -->
				<img src={logo} class="w-10">
				<!-- svelte-ignore a11y-missing-attribute -->
				<img src={ogo} class="w-20">
			</a>
		</div>
		<div class="flex-none">
			<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-label-has-associated-control -->
				<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
				<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
			<label tabindex="0" class="btn btn-circle ml-2 mr-2" on:click={handleBrowse}>
				<div class="indicator">
					<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="-2 -2 30 30"><path d="M21.172 24l-7.387-7.387c-1.388.874-3.024 1.387-4.785 1.387-4.971 0-9-4.029-9-9s4.029-9 9-9 9 4.029 9 9c0 1.761-.514 3.398-1.387 4.785l7.387 7.387-2.828 2.828zm-12.172-8c3.859 0 7-3.14 7-7s-3.141-7-7-7-7 3.14-7 7 3.141 7 7 7z"/></svg>
				</div>
			</label>
			{#if userType == 2}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-label-has-associated-control -->
				<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
				<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
				<label tabindex="0" class="btn btn-circle ml-2 mr-2" on:click={handleMap}>
					<div class="indicator">
						<svg width="24" height="24" xmlns="http://www.w3.org/2000/svg" fill-rule="evenodd" clip-rule="evenodd"><path d="M24 20l-6.455 4-5.545-4-5.545 4-6.455-4v-20l6.455 4 5.545-4 5.545 4 6.455-4v20zm-11.5-13h-1v-5.406l-4.5 3.246v4.16h-1v-4.106l-5-3.098v17.647l5 3.099v-6.542h1v6.374l4.5-3.246v-5.128h1v5.128l4.5 3.246v-5.374h1v5.542l5-3.099v-17.647l-5 3.098v3.106h-1v-3.16l-4.5-3.246v5.406zm8.172 7.016l-1.296-1.274 1.273-1.293-.708-.702-1.272 1.294-1.294-1.271-.703.702 1.296 1.276-1.273 1.296.703.703 1.277-1.298 1.295 1.275.702-.708zm-14.102-.606c-.373 0-.741-.066-1.092-.195l.407-1.105c.221.081.451.122.685.122.26 0 .514-.05.754-.149l.448 1.09c-.383.157-.787.237-1.202.237zm-2.601-2.374c-.535 0-.969.433-.969.968 0 .534.434.968.969.968.535 0 .969-.434.969-.968 0-.535-.434-.968-.969-.968zm11.271 1.591l-1.659-.945.583-1.024 1.66.945-.584 1.024zm-6.455-.02l-.605-1.011 1.638-.981.606 1.01-1.639.982zm3.918-1.408c-.243-.101-.5-.153-.763-.153-.231 0-.457.04-.674.118l-.402-1.108c.346-.125.708-.188 1.076-.188.419 0 .83.082 1.216.243l-.453 1.088z"/></svg>
					</div>
				</label>
			{/if}
			<div class="dropdown dropdown-end">
				<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
				<!-- svelte-ignore a11y-label-has-associated-control -->
				<label tabindex="0" class="btn btn-circle avatar">
					<div class="w-10 rounded-full">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 16 16" stroke="currentColor" transform="translate(10, 10)">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4" d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3Zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/>
						</svg>
					</div>
				</label>
				<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
				<ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
					<!-- svelte-ignore a11y-missing-attribute -->
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<!-- svelte-ignore a11y-no-static-element-interactions -->
					<li><a on:click={handleSettings}>Settings</a></li>
					<!-- svelte-ignore a11y-missing-attribute -->
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<!-- svelte-ignore a11y-no-static-element-interactions -->
					{#if userType == 1}
						<li><a on:click={handleOrders}>Orders</a></li>
					{/if}
					<!-- svelte-ignore a11y-missing-attribute -->
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<!-- svelte-ignore a11y-no-static-element-interactions -->
					<li><a on:click={handleLogout}>Logout</a></li>
				</ul>
			</div>
			{#if userType == 1}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-label-has-associated-control -->
				<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
				<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
				<label tabindex="0" class="btn btn-circle ml-2 mr-2" on:click={handleShoppingCart}>
					<div class="indicator">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
						</svg>
						<span class="badge badge-secondary badge-sm indicator-item">{numCartItemsState}</span>
					</div>
				</label>
			{/if}
		</div>
	</div>
{/if}