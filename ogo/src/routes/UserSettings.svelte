<script lang="ts">
    let usernameState = "Username";

    let changedUsernameState = "";
    let changedPasswordState = "";

    let storedChangedUsername = "";
    let storedChangedPassword = "";

    async function getUsername() {
        const currentUser = await fetch("/getUser", {
            method: "GET"
        })
        const currentUserJson = await currentUser.json();
        usernameState = currentUserJson.username;

        console.log(currentUserJson.username);

        document.getElementById('usernameDisplay')!.textContent = "Hello " + usernameState;
    }

    window.addEventListener('DOMContentLoaded', (e) => {
        getUsername();
    });
</script>

<html lang="en" data-theme="lemonade">
    <h1 id="usernameDisplay" class="card-title mt-4 ml-4">Hello {usernameState}</h1>
    <div class="ml-16 mt-4">
        <h1 class="card-title">Basic Information</h1>
        <div class="grid grid-cols-1 gap-4 ml-16 mb-16 mt-4">
            <div>
                <input type="text" placeholder="Username" class="input input-bordered w-full max-w-xs" />
                <button class="btn btn-secondary">Update</button>
            </div>
            <div>
                <input type="password" placeholder="Password" class="input input-bordered w-full max-w-xs" />
                <button class="btn btn-secondary">Update</button>
            </div>
        </div>
    </div>
</html>

<style>

</style>