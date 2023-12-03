<script lang="ts">
    import { onMount } from "svelte";
    import AddressAutocomplete from "../lib/components/AddressAutocomplete.svelte";
    import { getCurrentUser, updateUser } from "../lib/util/RequestController";
    import Navbar from "../lib/components/Navbar.svelte";

    import { alert } from '../lib/stores/alertStore';
    import AlertDaisy from "../lib/components/AlertDaisy.svelte";

    const MIN_PASSWORD_LENGTH = 1;
    const MAX_PASSWORD_LENGTH = 20;
    
    let user: any;
    let loggedInUserID: number;
    let isAdmin = false;

    let userList: any[] = [];

    let usernameState = "";
    let addressState = "";

    let changedUsernameState = "";
    let changedPasswordState = "";
    let changedPasswordState2 = "";
    let changedAddressState = "";

    let storedChangedUsername = "";
    let storedChangedPassword = "";
    let storedChangedAddress = "";

    async function getUser() {
        try {
            const result = await getCurrentUser();

            user = result.user;
            loggedInUserID = result.user.user_id;
            isAdmin = result.user.is_admin;

            usernameState = result.user.username;
            addressState = result.user.address;

            console.log(result.user);
        } catch (error) {
            console.error("Error fetching user:", error);
        }
    }

    async function handleNewUsername() {
        storedChangedUsername = changedUsernameState;
        if (storedChangedUsername.length == 0) {
           return;
        }

        const userData = {
            "username": storedChangedUsername,
        }

        console.log(userData);
        
        try {
            let update = await updateUser(userData);
            if (update.success){
                await getUser();
                alert.set({ show: true, message: `Updated username to ${user.username}`, type: 'success'});
                changedUsernameState = "";
            }else{
                alert.set({ show: true, message: "Error: " + update.message, type: 'error'});
                changedUsernameState = "";
            }
        } catch (error) {
            console.error("Error updating username:", error);
            alert.set({ show: true, message: 'Error updating username: ' + error, type: 'error'});
        }
    }

    async function handleNewPassword() {
        if (changedPasswordState2 != changedPasswordState) {
            alert.set({ show: true, message: 'Passwords must match', type: 'error'});
            changedPasswordState2 = "";
            return;
        }
        if (changedPasswordState.length === 0 || changedPasswordState2.length === 0) {
           return;
        }
        if (changedPasswordState.length > MAX_PASSWORD_LENGTH || changedPasswordState2.length > MAX_PASSWORD_LENGTH) {
            alert.set({ show: true, message: 'Password must be 1-20 characters', type: 'error'});
            changedPasswordState2 = "";
            return;
        }

        storedChangedPassword = changedPasswordState;
        const userData = {
            "password": storedChangedPassword
        }

        console.log(userData);

        try {
            await updateUser(userData);
            await getUser();
            alert.set({ show: true, message: 'Updated password', type: 'success'});
            changedPasswordState = "";
            changedPasswordState2 = "";
        } catch (error) {
            console.error("Error updating password:", error);
            alert.set({ show: true, message: 'Error updating password: ' + error, type: 'error'});
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
            alert.set({ show: true, message: 'Updated address', type: 'success'});
            changedAddressState = "";
        } catch (error) {
            console.error("Error updating address:", error);
            alert.set({ show: true, message: 'Error updating address: ' + error, type: 'error'});
        }
    }

    function handlePlaceSelect(place: string) {
        changedAddressState = place;
    }

    async function fetch_users() {
        try {
            const request = await fetch("/getAllUsers");
            userList = await request.json();
        } catch (error) {
            console.log("error: ", error);
        }
    }

    function demote_user(user_id: number) {
      console.log("Demoting user: " + user_id);
      fetch('/demoteUser', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"user_id": user_id}),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response;
      })
      .then(data => {
        console.log('Response:', data);
        userList.find((u:any) => u.user_id == user_id).is_admin = false;
        userList = userList.slice();
      })
      .catch(error => {
        console.error('Error:', error.message);
      });

    }

    function promote_user(user_id: number) {
      console.log("promoting user: " + user_id);
      fetch('/promoteUser', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"user_id": user_id}),
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response;
      })
      .then(data => {
        console.log('Response:', data);
        userList.find((u:any) => u.user_id == user_id).is_admin = true;
        userList = userList.slice();
      })
      .catch(error => {
        console.error('Error:', error.message);
      });

    }
    // get user immediately upon component mount
    onMount(async() => {
        await getUser();

        if (isAdmin) {
            await fetch_users();
        }
    });
</script>

<html lang="en" data-theme="lemonade">
    <Navbar/>
    <AlertDaisy {alert} />
    <div class="relative min-w-screen h-screen flex-grow flex flex-col px-4 sm:px-0">
        <div class="card min-w-screen bg-base-100 border-2 border-black-500 m-6 mb-3 shadow-md">
            <div class="card-body overflow-x-auto">
                <h1 class="card-title">Account Information</h1>
                <table class="table">
                    <tbody>
                        <tr>
                            <th>Username</th>
                            <td colspan="2">
                                <input
                                    type="text"
                                    placeholder={usernameState}
                                    bind:value={changedUsernameState}
                                    class="input input-bordered w-full"
                                />
                            </td>
                            <td>
                                <button on:click={handleNewUsername} class="btn btn-secondary">Update</button>
                            </td>
                        </tr>
                        <tr>
                            <th>Address</th>
                            <td colspan="2">
                                <AddressAutocomplete placeholder={addressState} onPlaceSelect={handlePlaceSelect}/> 
                            </td>
                            <td>
                                <button on:click={handleNewAddress} class="btn btn-secondary">Update</button>
                            </td>
                        </tr>
                        <tr>
                            <th>Password</th>
                            <td>
                                <input
                                    type="password"
                                    placeholder="password"
                                    bind:value={changedPasswordState}
                                    class="input input-bordered w-full"
                                />   
                            </td>
                            <td>
                                <input
                                    type="password"
                                    placeholder="re-enter password"
                                    bind:value={changedPasswordState2}
                                    class="input input-bordered w-full"
                                />   
                            </td>
                            <td>
                                <button on:click={handleNewPassword} class="btn btn-secondary max-w-md">Update</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        {#if isAdmin}
            <div class="card min-w-screen bg-base-100 border-2 border-black-500 m-6 mt-3 shadow-md">
                <div class="card-body overflow-x-auto">
                    <div class="card-title">User List</div>
                    <table class="table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Address</th>
                                <th>Role</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each  userList as u}
                                <tr class="hover">
                                    <th>{u.user_id}</th>
                                    <td>{u.username}</td>
                                    <td>{u.address}</td>
                                    <td>
                                        {u.is_admin ? "Employee": "Customer"} &nbsp;
                                        {#if u.user_id == loggedInUserID}
                                            <button class="btn btn-xs btn-disabled">You</button>
                                        {:else if u.is_admin}
                                            <button class="btn btn-xs btn-primary" on:click={() => demote_user(u.user_id)}>Demote</button>
                                        {:else}
                                            <button class="btn btn-xs btn-error" on:click={() => promote_user(u.user_id)}>Promote</button>
                                        {/if}
                                    </td>
                                </tr>
                            {/each}       
                        </tbody>
                    </table>
                </div>
            </div>
        {/if}
    </div>
</html>