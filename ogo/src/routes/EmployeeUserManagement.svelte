<script lang="ts">
  import { onMount } from "svelte";
    import Navbar from "../lib/components/Navbar.svelte";

    let userList: any[] = [];
    let loggedInUserID: number;

    async function fetch_users(){
        try{
            const request = await fetch("/getAllUsers");
            userList = await request.json();
        } catch (error){
            console.log("error: ", error);
        }
    }

    async function fetch_user_id(){
        try{
            const request = await fetch("/getUser");
            loggedInUserID = (await request.json()).user_id;
        } catch (error){
            console.log("error: ", error);
        }
    }

    function demote_user(user_id: number){
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

    function premote_user(user_id: number){
      console.log("premoting user: " + user_id);
      fetch('/premoteUser', {
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
    
    onMount(async ()=>{
        await fetch_user_id();
        await fetch_users();
    })
    

</script>

<style>
  body {
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
  } 
</style>

<body>
  <Navbar/>
  <div class="card card-normal card-bordered mx-4 my-4">
      <div class="card-body">
        <div class="card-title">User List</div>
        <table class="table table-md">
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
                  <button class="btn btn-xs	btn-disabled">You</button>
                  {:else if u.is_admin}
                    <button class="btn btn-xs	btn-primary" on:click={() => demote_user(u.user_id)}>Demote</button>
                  {:else}
                    <button class="btn btn-xs	btn-error" on:click={() => premote_user(u.user_id)}>Premote</button>
                  {/if}
                </td>
              </tr>
            {/each}       
          </tbody>
        </table>
      </div>
  </div>
</body>