<script lang="ts">
    // TODO: Signup page should not show/work for already logged-in users

    import { navigate } from 'svelte-routing';

    let usernameState = "";
    let passwordState = "";
    let toggleIsCheckedState = false;

    let storedUsername = "";
    let storedPassword = "";

    let signupErrorState = false;
    let signupErrorTextState = "";
    let signupErrorModal: HTMLDialogElement;

    $: if (signupErrorState) {
        showSignupErrorModal();
    }

    function showSignupErrorModal() {
        signupErrorModal.showModal();
    }

    function closeSignupErrorModal() {
        signupErrorModal.close();
        signupErrorState = false;
    }
    
    async function handleSubmit() {
        storedUsername = usernameState;
        storedPassword = passwordState;

        console.log(storedUsername);
        console.log(storedPassword);

        if (storedUsername.length == 0 && storedPassword.length == 0) {
            signupErrorTextState = "Cannot have a blank username or password.";
            signupErrorState = true;
        } else if (storedUsername.length <= 20 && storedPassword.length <= 20) {
            const signupResponse = await fetch("/signup", {
                method: "POST",
                headers: {
                'Content-Type': "application/json"
                },
                body: JSON.stringify({
                    "username": storedUsername,
                    "password": storedPassword,
                    "address": ""
                })
            })

            // signup success or fail
            if (signupResponse.ok) {
                const message = await signupResponse.text();
                console.log(message);
                navigate("/home");
            } else {
                console.error("Error signing up:", await signupResponse.text());
            }
            
            // test getUser
            const currentUser = await fetch("/getUser", {
                method: "GET"
            })
            const currentUserJson = await currentUser.json();
            const currentUserResult = JSON.stringify(currentUserJson);

            console.log(currentUserResult);

        } else {
            signupErrorTextState = "Username and password must be less than 20 characters.";
            signupErrorState = true;
        }
    }

    async function handleToggle() {
        toggleIsCheckedState = !toggleIsCheckedState;
        // TODO: switch customer/employee
    }
</script>

<html lang="en" data-theme="lemonade">
    <div class="min-w-screen flex flex-col items-center justify-center bg-gray-200">
        <div class="card w-96 bg-base-100 border-2 border-black-500 mt-8">
            <dialog bind:this={signupErrorModal} class="modal">
                <div class="modal-box bg-red-300">
                    <h3 class="font-bold text-lg">Error!</h3>
                    <p class="py-4">{signupErrorTextState}</p>
                </div>
                <form method="dialog" class="modal-backdrop">
                    <button on:click={closeSignupErrorModal}>close</button>
                </form>
            </dialog>
            <div class="card-body">
                <div class="flex justify-between items-center">
                    <h1 class="card-title">SIGN UP</h1>
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
            Returning user? Login <a href="/login"><u>here</u></a>
        </p>
    </div>
</html>

<style>

</style>