<script lang="ts">
	import logo from "../assets/logo.png";
	import { onMount } from 'svelte';
    import { navigate } from 'svelte-routing';

	onMount(async () => {
        navigate("/");    
    });
</script>

<!--<img src={logo} alt="logo.png" class="w-24 h-24"/>-->