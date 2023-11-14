<script lang="ts">
    // TODO: Signup page should not show/work for already logged-in users

    import bg from "../assets/bg1.jpeg";
    import { signup } from "../lib/util/RequestController"
    import { navigate } from 'svelte-routing';
    import { onMount } from 'svelte';

    let usernameState = "";
    let passwordState = "";
    let passwordState2 = "";
    let toggleIsCheckedState = false;

    let storedUsername = "";
    let storedPassword = "";

    //let signupErrorState = false;
    //let signupErrorTextState = "";
    //let signupErrorModal: HTMLDialogElement;

    import { alert } from '../lib/stores/alertStore';
    import AlertDaisy from "../lib/components/AlertDaisy.svelte";

    /*
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
    */
    
    async function handleSubmit() {
        if (passwordState2 != passwordState) {
            alert.set({ show: true, message: 'Passwords must match', type: 'warning'});
            return;
        }
        if (passwordState2.length == 0) {
            alert.set({ show: true, message: 'User must have password', type: 'warning'});
            return;
        }
        if (usernameState.length == 0) {
            alert.set({ show: true, message: 'User must have username', type: 'warning'});
            return;
        }
        storedUsername = usernameState;
        storedPassword = passwordState;

        console.log(storedUsername);
        console.log(storedPassword);

        const result = await signup(storedUsername, storedPassword, "", toggleIsCheckedState); // TODO: address?

        if (result.success) {
            console.log("Signed up successfully!", JSON.stringify(result.user));
            alert.set({ show: true, message: 'Welcome ' + storedUsername + '!', type: 'success'});
            navigate("/login");
        } else {
            console.error("Signup failed:", result.message);
            //signupErrorTextState = result.message;
            //signupErrorState = true;
            alert.set({ show: true, message: 'Signup failed: ' + result.message, type: 'error'});
        }
    }

    async function handleToggle() {
        toggleIsCheckedState = !toggleIsCheckedState;
        // TODO: switch customer/employee
    }

    onMount(() => {
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
        <AlertDaisy {alert} />
        <div class="card w-full sm:w-3/4 md:w-1/2 lg:w-1/3 xl:w-96 bg-base-100 border-2 border-black-500 mt-8">
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
                    <!-- svelte-ignore a11y-label-has-associated-control -->
                    <label class="label">
                        <span class="label-text">Re-enter Password</span>
                    </label>
                    <input bind:value={passwordState2} type="password" class="input input-bordered w-full max-w-xs" />
                </div>
                <button on:click={handleSubmit} class="btn bg-secondary mt-6">Submit</button>
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-no-static-element-interactions -->
                <!-- svelte-ignore a11y-missing-attribute -->
                <a on:click={() => navigate('/login')} class="text-primary hover:underline cursor-pointer text-center">Returning user? Login here!</a>
            </div>
        </div>
    </div>
</html>

<style>

</style>