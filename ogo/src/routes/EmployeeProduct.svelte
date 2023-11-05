<script lang="ts">
	import productImage from "../assets/logo_icon.png";

	let productId = 1;

	let productNameState = "";
	let priceState = "";
	let sizeState = "";
	let weightState = "";
	let productDescriptionState = "";

	let storedProductName = "";
	let storedPrice = "";
	let storedSize = "";
	let storedWeight = "";
	let storedProductDescription = "";

	async function testCreateProduct() {
		const createProductResponse = await fetch("/createProduct", {
            method: "POST",
            headers: {
            'Content-Type': "application/json"
            },
            body: JSON.stringify({
                "name": "Apple",
                "description": "An apple is a fruit.",
				"image": "",
				"quantity": 1,
				"price": 1.29,
				"weight": 0.5
            })
        })
		if (createProductResponse.ok) {
			const message = await createProductResponse.text();
			console.log(message);
		} else {
			console.error("Error creating product:", await createProductResponse.text());
		}

		const getProductsResponse = await fetch("/getProducts", {
            method: "GET"
        })
        const json = await getProductsResponse.json();
        const result = JSON.stringify(json);
        console.log(result);
	}

	async function handleApplyChanges() {
		storedProductName = productNameState;
		storedPrice = priceState;
		storedSize = sizeState;
		storedWeight = weightState;
		storedProductDescription = productDescriptionState;

		console.log(storedProductName);
		console.log(storedPrice);
		console.log(storedSize);
		console.log(storedWeight);
		console.log(storedProductDescription);

		const updateProductResponse = await fetch("/updateProduct", {
            method: "POST",
            headers: {
            'Content-Type': "application/json"
            },
            body: JSON.stringify({
                "product_id": productId,
                "name": storedProductName,
                "description": storedProductDescription,
				"image": "",
				"quantity": 0,
				"price": 0,
				"weight": 0
            })
        })
		if (updateProductResponse.ok) {
			const message = await updateProductResponse.text();
			console.log(message);
		} else {
			console.error("Error updating product:", await updateProductResponse.text());
		}

		const getProductsResponse = await fetch("/getProducts", {
            method: "GET"
        })
        const json = await getProductsResponse.json();
        const result = JSON.stringify(json);
        console.log(result);
	}
</script>

<html lang="en" data-theme="lemonade">
	<div class="flex flex-col w-full">
		<div class="grid h-max flex-grow card bg-gray-200 rounded-box place-items-center">
			<div class="card w-96 max-w-xs bg-base-100 shadow-xl mt-6 mb-12">
				<!-- svelte-ignore a11y-missing-attribute -->
				<figure><img src={productImage}/></figure>
			</div>
		</div>
		
		<div class="grid h-max flex-grow card bg-gray-200 rounded-box place-items-center">
			<div class="form-control w-full max-w-2xl">
				<!-- svelte-ignore a11y-label-has-associated-control -->
				<label class="label">
					<span class="label-text">Product Name</span>
				</label>
				<input bind:value={productNameState} type="text" placeholder="" class="input input-bordered w-full" />
			</div>
		
			<div class="form-control w-full max-w-2xl">
				<!-- svelte-ignore a11y-label-has-associated-control -->
				<label class="label">
					<span class="label-text">Price</span>
				</label>
				<input bind:value={priceState} type="text" placeholder="" class="input input-bordered w-full max-w-xs" />
			</div>
		
			<div class="form-control w-full max-w-2xl">
				<!-- svelte-ignore a11y-label-has-associated-control -->
				<label class="label">
					<span class="label-text">Size</span>
				</label>
				<input bind:value={sizeState} type="text" placeholder="" class="input input-bordered w-full max-w-xs" />
			</div>
		
			<div class="form-control w-full max-w-2xl">
				<!-- svelte-ignore a11y-label-has-associated-control -->
				<label class="label">
					<span class="label-text">Weight</span>
				</label>
				<input bind:value={weightState} type="text" placeholder="" class="input input-bordered w-full max-w-xs" />
			</div>
		
			<div class="form-control w-full max-w-2xl">
				<!-- svelte-ignore a11y-label-has-associated-control -->
				<label class="label">
					<span class="label-text">Product Description</span>
				</label>
				<textarea bind:value={productDescriptionState} class="textarea textarea-bordered w-full h-48" placeholder=""></textarea>
			</div>

			<button on:click={testCreateProduct} class="btn bg-accent mt-6 mb-6">Test</button>

			<button on:click={handleApplyChanges} class="btn bg-secondary mt-6 mb-6">Apply Changes</button>
		</div>
	</div>
</html>

<style>

</style>