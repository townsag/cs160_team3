<script lang="ts">
    let usernameState = "";
    let toggleIsCheckedState = false;

    let storedUsername = "";
    
    function handleSubmit() {
        storedUsername = usernameState;
        console.log(storedUsername);
    }

    function handleToggle() {
        toggleIsCheckedState = !toggleIsCheckedState;
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
                    <input type="text" class="input input-bordered w-full max-w-xs" />
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