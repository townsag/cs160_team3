<script  lang="ts">
    import { onMount } from "svelte";
    import { Loader } from "@googlemaps/js-api-loader";
    import { fetchApiKey } from "../util/RequestController";

    export let onPlaceSelect: ((place: any) => void) | undefined;

    const loadGoogleMaps = async () => {
        try {
            const result = await fetchApiKey();
        
            const loader = new Loader({
                apiKey: result.API_KEY,
                version: "weekly",
                libraries: ["places"],
            });

            await loader.importLibrary("places");
            initAutocomplete();
        } catch (error) {
            console.error("Error loading Google Maps API:", error);
        }
    };

    const initAutocomplete = () => {
        const input = document.getElementById("autocomplete") as HTMLInputElement;
        const autocomplete = new google.maps.places.Autocomplete(input);

        autocomplete.addListener("place_changed", () => {
            const place = autocomplete.getPlace();
            console.log("Selected place:", place);
            if (onPlaceSelect) {
                onPlaceSelect(place);
            }
        });
    };

    onMount(loadGoogleMaps);
</script>

<html lang="en" data-theme="lemonade">
    <input
        type="text"
        id="autocomplete"
        placeholder="Address"
        class="input input-bordered w-full max-w-xs"
    />
</html>

<style>

</style>