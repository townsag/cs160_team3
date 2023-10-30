<script lang="ts">
    // TODO: Login page should not show/work for already logged-in users


    import { login, getCurrentUser } from "../lib/util/RequestController"
    import { navigate } from 'svelte-routing';

    let usernameState = "";
    let passwordState = "";
    let toggleIsCheckedState = false;

    let storedUsername = "";
    let storedPassword = "";

    let bg = "https://user-images.githubusercontent.com/63530023/278915388-7232c29c-49d0-49b6-bd28-e26c65f36783.jpeg";
    
    async function handleSubmit() {
        storedUsername = usernameState;
        storedPassword = passwordState;

        console.log(storedUsername);
        console.log(storedPassword);

        const result = await login(storedUsername, storedPassword);

        if (result.success) {
            console.log("Logged in successfully!");
            navigate("/home");
        } else {
            console.error("Login failed:", result.message);
        }

        const userResult = await getCurrentUser();

        if (userResult.success) {
            console.log('User data:', userResult.user.user_id, userResult.user.username);
        } else {
            console.error('Error fetching user:', result.message);
        }
    }

    async function handleToggle() {
        toggleIsCheckedState = !toggleIsCheckedState;
    }
</script>

<html lang="en" data-theme="lemonade">
    <div class="relative min-w-screen h-screen flex-grow flex flex-col items-center justify-center px-4 sm:px-0"
     style="background-image: url({bg}); background-size: cover; background-repeat: no-repeat;">
        <div class="absolute inset-0 bg-white bg-opacity-50 backdrop-blur-md backdrop-contrast-125"></div>
        <div class="card w-full sm:w-3/4 md:w-1/2 lg:w-1/3 xl:w-96 bg-base-100 border-2 border-black-500 mt-8">
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