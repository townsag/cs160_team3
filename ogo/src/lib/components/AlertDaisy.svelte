<script lang="ts">
    import { alert } from '../stores/alertStore';

    /* to use on other pgs u must have
		// in script
            // for declaring and importing values
			    import { alert } from '../lib/stores/alertStore';
                import AlertDaisy from "../lib/components/AlertDaisy.svelte";
            // for everytime you call a alert (like diff alerts)
                alert.set({ show: true, message: '[YOUR ALERT MSG]', type: '[error|success|warning]'});
        // in html
            <AlertDaisy {alert} />
	*/

    let timer: any;
    const closeAlert = () => {
        alert.update((value) => ({ ...value, show: false }));
    };

    $: {
        if ($alert.show) {
            clearTimeout(timer);
            timer = setTimeout(closeAlert, 2000);
        }
    }
</script>

<style>
    .alert {
        position: fixed;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        width: 500px;
        z-index: 1000;
    }
</style>

{#if $alert.show}
    {#if $alert.type === "error"} 
        <div class="alert alert-error">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            <span>{$alert.message}</span>
        </div>
    {:else if $alert.type === "success"} 
        <div class="alert alert-success">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            <span>{$alert.message}</span>
        </div>
    {:else}
        <div class="alert alert-warning">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
            <span>{$alert.message}</span>
        </div>
    {/if}
{/if}