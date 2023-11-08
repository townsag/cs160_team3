<script lang="ts">
    import { onMount } from "svelte";
    import { getCurrentUser, updateUser } from "../lib/util/RequestController"
    
    let user: any;
    let usernameState = "Username";

    let changedUsernameState = "";
    let changedPasswordState = "";
    let changedAddressState = "";

    let storedChangedUsername = "";
    let storedChangedPassword = "";
    let storedChangedAddress = "";

    async function getUser() {
        try {
            const result = await getCurrentUser();

            user = result.user;
            usernameState = result.user.username;

            console.log(result.user);
        } catch (error) {
            console.error("Error fetching user:", error);
        }
    }

    async function handleNewUsername() {
        storedChangedUsername = changedUsernameState;

        const userData = {
            "username": storedChangedUsername,
        }

        console.log(userData);

        try {
            await updateUser(userData);
            await getUser();
        } catch (error) {
            console.error("Error updating username:", error);
        }
    }

    async function handleNewPassword() {
        storedChangedPassword = changedPasswordState;

        const userData = {
            "username": user.username,
            "password": storedChangedPassword
        }

        console.log(userData);

        try {
            await updateUser(userData);
            await getUser();
        } catch (error) {
            console.error("Error updating password:", error);
        }
    }

    async function handleNewAddress() {
        storedChangedAddress = changedAddressState;

        const userData = {
            "address": storedChangedAddress,
        }

        console.log(userData);

        try {
            await await updateUser(userData);
            await getUser();
        } catch (error) {
            console.error("Error updating address:", error);
        }
    }

    // get user immediately upon component mount
    onMount(async() => {
        await getUser();
    });
</script>

<html lang="en" data-theme="lemonade">
    <h1 id="usernameDisplay" class="card-title mt-4 ml-4">Hello {usernameState}</h1>
    <div class="ml-16 mt-4">
        <h1 class="card-title">Basic Information</h1>
        <div class="grid grid-cols-1 gap-4 ml-16 mb-16 mt-4">
            <div>
                <input
                    type="text"
                    placeholder="Username"
                    bind:value={changedUsernameState}
                    class="input input-bordered w-full max-w-xs"
                />

                <button on:click={handleNewUsername} class="btn btn-secondary">Update</button>
            </div>

            <div>
                <input
                    type="password"
                    placeholder="Password"
                    bind:value={changedPasswordState}
                    class="input input-bordered w-full max-w-xs"
                />

                <button on:click={handleNewPassword} class="btn btn-secondary">Update</button>
            </div>

            <div>
                <input
                    type="text"
                    placeholder="Address"
                    bind:value={changedAddressState}
                    class="input input-bordered w-full max-w-xs"
                />

                <button on:click={handleNewAddress} class="btn btn-secondary">Update</button>
            </div>
        </div>
    </div>
</html>

<style>

</style>