<script lang="ts">

</script>

<html lang="en" data-theme="lemonade">
    <div class="min-w-screen flex flex-col items-center justify-center m-8">
        <div class="card w-96 bg-base-100 border-2 border-black-500">
            <div class="card-body">
                <h2 class="card-title">LOGIN</h2>
                <div class="form-control w-full max-w-xs">
                    <!-- svelte-ignore a11y-label-has-associated-control -->
                    <label class="label">
                        <span class="label-text">Username</span>
                    </label>
                    <input type="text" class="input input-bordered w-full max-w-xs" />
                     <!-- svelte-ignore a11y-label-has-associated-control -->
                    <label class="label">
                        <span class="label-text">Password</span>
                    </label>
                    <input type="text" class="input input-bordered w-full max-w-xs" />
                </div>
                <button class="btn bg-secondary mt-6">Submit</button>
            </div>
        </div>
        <p class="mt-6">
            New user? Sign up <a href="/signup"><u>here</u></a>
        </p>
    </div>
</html>

<style>

</style>