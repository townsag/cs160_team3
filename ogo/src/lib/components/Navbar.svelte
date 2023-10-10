<script lang="ts">
	// import logo from "../../assets/logo_icon.png";

	async function handleLogout() {
        const logoutResult = await fetch("/logout", {
            method: "GET"
        });

        if (logoutResult.ok) {
            const message = await logoutResult.text();
            console.log(message);
        } else {
            console.error("Failed to logout.");
        }
	}
</script>

<div class="navbar bg-base-100">
	<div class="flex-1">
		<a class="btn btn-ghost normal-case text-xl" href="/">OGO</a>
	</div>
	<div class="flex-none">
		<div class="dropdown dropdown-end">
			<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
			<!-- svelte-ignore a11y-label-has-associated-control -->
			<label tabindex="0" class="btn btn-ghost btn-circle avatar">
			  <div class="w-10 rounded-full">
				<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 16 16" stroke="currentColor" transform="translate(10, 10)">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4" d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3Zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/>
				  </svg>
			  </div>
			</label>
			<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
			<ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
			  <!-- svelte-ignore a11y-missing-attribute -->
			  <li><a>Settings</a></li>
			  <!-- svelte-ignore a11y-missing-attribute -->
			  <!-- svelte-ignore a11y-click-events-have-key-events -->
			  <!-- svelte-ignore a11y-no-static-element-interactions -->
			  <li><a on:click={handleLogout}>Logout</a></li>
			</ul>
		  </div>
	  <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
	  <div class="dropdown dropdown-end">
		<!-- svelte-ignore a11y-label-has-associated-control -->
		<label tabindex="0" class="btn btn-ghost btn-circle">
		  <div class="indicator">
			<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
			<span class="badge badge-sm indicator-item bg-secondary border-0">8</span>
		  </div>
		</label>
		<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
		<div tabindex="0" class="mt-3 z-[1] card card-compact dropdown-content w-52 bg-base-100 shadow">
		  <div class="card-body">
			<span class="font-bold text-lg">8 Items</span>
			<span class="text-info">Subtotal: $999</span>
			<div class="card-actions">
			  <button class="btn btn-primary btn-block">View cart</button>
			</div>
		  </div>
		</div>
	  </div>
	</div>
  </div>
  <div class="divider mt-0 mb-0"></div> 