<script lang="ts">
    import { navigate } from 'svelte-routing';

    let usernameState = "";
    let passwordState = "";
    let toggleIsCheckedState = false;

    let storedUsername = "";
    let storedPassword = "";
    
    async function handleSubmit() {
        storedUsername = usernameState;
        storedPassword = passwordState;

        console.log(storedUsername);
        console.log(storedPassword);

        const loginResponse = await fetch("/login", {
            method: "POST",
            headers: {
            'Content-Type': "application/json"
            },
            body: JSON.stringify({
                "username": storedUsername,
                "password": storedPassword,
            })
        })
        
        if (loginResponse.ok) {
            const message = await loginResponse.text();
            console.log(message);
            navigate("/home");
        } else {
            console.error("Failed to login.");
        }

        // Test
        // const products = await fetch("/getProducts", {
        //     method: "GET"
        // })
        // const json = await products.json();
        // const result = JSON.stringify(json);

        // console.log(result);
    }

    async function handleToggle() {
        toggleIsCheckedState = !toggleIsCheckedState;

        // Test
        // const post = await fetch("/createProduct", {
        //     method: "POST",
        //     headers: {
        //     'Content-Type': 'application/json;charset=utf-8'
        //     },
        //     body: JSON.stringify({
        //         "name": "Test product",
        //         "description": "Description for test product",
        //         "image": "www.google.com",
        //         "quantity": 1,
        //         "price": 1.00,
        //         "weight": 1.0
        //     })
        // })

        // console.log(post);
        // TODO: switch customer/employee
    }
</script>

<html lang="en" data-theme="lemonade">
    <div class="min-w-screen flex flex-col items-center justify-center bg-gray-200">
        <div class="card w-96 bg-base-100 border-2 border-black-500 mt-8">
            <div class="card-body">
                <div class="flex justify-between items-center">
                    <h1 class="card-title">LOGIN</h1>
                    <div class="flex">
                        <h2 class="mr-2">{toggleIsCheckedState ? "Employee" : "Customer"}</h2>
                        <input on:click={handleToggle} type="checkbox" class="toggle toggle-primary" />
                    </div>
                </div>
                <div class="form-control w-full max-w-xs">
                    <!-- svelte-ignore a11y-label-has-associated-control -->
                    <label class="label">
                        <span class="label-text">Username</span>
                    </label>
                    <input bind:value={usernameState} type="text" class="input input-bordered w-full max-w-xs" />
                     <!-- svelte-ignore a11y-label-has-associated-control -->
                    <label class="label">
                        <span class="label-text">Password</span>
                    </label>
                    <input bind:value={passwordState} type="password" class="input input-bordered w-full max-w-xs" />
                </div>
                <button on:click={handleSubmit} class="btn bg-secondary mt-6">Submit</button>
            </div>
        </div>
        <p class="m-8">
            New user? Sign up <a href="/signup"><u>here</u></a>
        </p>
    </div>
</html>

<style>

</style>