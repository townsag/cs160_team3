<script lang="ts">
    // TODO: Login page should not show/work for already logged-in users

    import bg from "../assets/bg1.jpeg";
    import { login, getCurrentUser } from "../lib/util/RequestController"
    import { navigate } from 'svelte-routing';
    import { onMount } from 'svelte';
    import AlertDaisy from "../lib/components/AlertDaisy.svelte";

    let usernameState = "";
    let passwordState = "";
    let toggleIsCheckedState = false;

    let storedUsername = "";
    let storedPassword = "";

    let alertShow = false;
    let alertMsg = "";
    let alertType = "";
    function toggleShow() {
        alertShow = false;
    }
    
    async function handleSubmit() {
        storedUsername = usernameState;
        storedPassword = passwordState;

        console.log(storedUsername);
        console.log(storedPassword);

        const result = await login(storedUsername, storedPassword);

        if (result.success) {
            console.log("Logged in successfully!");
            navigate("/browse");
        } else {
            console.error("Login failed:", result.message);
            passwordState = '';
            alertShow = true;
            alertMsg = "Login failed: wrong password or username";
            alertType = "error";
        }

        const userResult = await getCurrentUser();

        if (userResult.success) {
            console.log('User data:', userResult.user.user_id, userResult.user.username);
        } else {
            console.error('Error fetching user:', result.message);
        }
    }

    async function sequential_api_calls(){
		try{                                  //getUser
			const response = await fetch("/getUser", { method: "GET" });
			const data = await response.json();
            navigate("/browse");
		} catch (error) {
		}
	}

    onMount(() => {
        sequential_api_calls();
        document.addEventListener('keydown', handleKeyDown);
        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        };
    });

    function handleKeyDown(event: any) {
        if (event.key === 'Enter') {
            // Check which input is focused and trigger the corresponding action
            const activeElement = document.activeElement;
            if (activeElement.tagName === 'INPUT') {
                handleSubmit();
            }
        }
    }
</script>

<html lang="en" data-theme="lemonade">
    <div class="relative min-w-screen h-screen flex-grow flex flex-col items-center justify-center px-4 sm:px-0"
     style="background-image: url({bg}); background-size: cover; background-repeat: no-repeat;">
        <div class="absolute inset-0 bg-white bg-opacity-50 backdrop-blur-md backdrop-contrast-125"></div>
        <AlertDaisy
            {alertShow}
            {alertMsg}
            {alertType}
            {toggleShow}
        />
        <div class="card w-full sm:w-3/4 md:w-1/2 lg:w-1/3 xl:w-96 bg-base-100 border-2 border-black-500 mt-8">
            <div class="card-body">
                <div class="flex justify-between items-center">
                    <h1 class="card-title">LOGIN</h1>
                    <!-- <div class="flex">
                        <h2 class="mr-2">{toggleIsCheckedState ? "Employee" : "Customer"}</h2>
                        <input on:click={handleToggle} type="checkbox" class="toggle toggle-primary" />
                    </div> -->
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
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-no-static-element-interactions -->
                <!-- svelte-ignore a11y-missing-attribute -->
                <a on:click={() => navigate('/signup')} class="text-primary hover:underline cursor-pointer text-center">New user? Sign up here!</a>
            </div>
        </div>
    </div>
</html>
