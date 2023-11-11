<script lang="ts">
    import { onMount } from "svelte";
    import AddressAutocomplete from "../lib/components/AddressAutocomplete.svelte"
    import { getCurrentUser, updateUser } from "../lib/util/RequestController"
    
    let user: any;

    let usernameState = "";
    let addressState = "";

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
            addressState = result.user.address;

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
        storedChangedAddress = changedAddressState || "";

        const userData = {
            "address": storedChangedAddress,
        }

        console.log(userData);

        try {
            await updateUser(userData);
            await getUser();
        } catch (error) {
            console.error("Error updating address:", error);
        }
    }

    function handlePlaceSelect(place: string) {
        changedAddressState = place;
    }

    // get user immediately upon component mount
    onMount(async() => {
        await getUser();
    });
</script>

<html lang="en" data-theme="lemonade">
    <div class="relative min-w-screen h-screen flex-grow flex flex-col px-4 sm:px-0">
        <h1 id="usernameDisplay" class="card-title p-8 pb-4">Hello {usernameState}!</h1>

        <div class="card min-w-screen bg-base-100 border-2 border-black-500 m-8">
            <div class="card-body">
                <h1 class="card-title">Account Information</h1>

                <div class="grid grid-cols-1 gap-4 p-4">
                    <div>
                        <!-- svelte-ignore a11y-label-has-associated-control -->
                        <label class="label">
                            <span class="label-text">Username</span>
                        </label>

                        <input
                            type="text"
                            placeholder={usernameState}
                            bind:value={changedUsernameState}
                            class="input input-bordered w-full max-w-md"
                        />
                    </div>

                    <div class="flex flex-row-reverse w-full max-w-md">
                        <button on:click={handleNewUsername} class="btn btn-secondary">Update</button>
                    </div>

                    <div>
                        <!-- svelte-ignore a11y-label-has-associated-control -->
                        <label class="label">
                            <span class="label-text">Password</span>
                        </label>

                        <input
                            type="password"
                            bind:value={changedPasswordState}
                            class="input input-bordered w-full max-w-md"
                        />                    
                    </div>

                    <div class="flex flex-row-reverse w-full max-w-md">
                        <button on:click={handleNewPassword} class="btn btn-secondary">Update</button>
                    </div>

                    <div>
                        <!-- svelte-ignore a11y-label-has-associated-control -->
                        <label class="label">
                            <span class="label-text">Address</span>
                        </label>
                        
                        <AddressAutocomplete placeholder={addressState} onPlaceSelect={handlePlaceSelect} />                 
                    </div>

                    <div class="flex flex-row-reverse w-full max-w-md">
                        <button on:click={handleNewAddress} class="btn btn-secondary max-w-md">Update</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</html>

<style>

</style>