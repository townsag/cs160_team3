<script lang="ts">
	import ogo from "../../assets/ogo.png";
	import logo from "../../assets/logo_icon.png";
	import { logout } from "../util/RequestController"
	import { navigate } from 'svelte-routing';
	import { onMount } from 'svelte';

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

	function handleSettings() {
		navigate("/settings");
	}

	function handleShoppingCart() {
		navigate("/cart");
	}
	function handleOrders() {
		if (userType == 2) {
			navigate("/employeesmaps");
		}
		console.log("go to customer order history");
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
		}
	}

	onMount(async () => {
        sequential_api_calls();       
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
					<li><a on:click={handleOrders}>Orders</a></li>
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
					</div>
				</label>
			{/if}
		</div>
	</div>
{/if}