<script  lang="ts">
    import { onMount } from "svelte";
    import { Loader } from "@googlemaps/js-api-loader";
    import { fetchApiKey } from "../util/RequestController";

    export let placeholder: string;
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

            console.log("Selected place:", place.formatted_address);
            if (onPlaceSelect) {
                onPlaceSelect(place.formatted_address);
            }
        });
    };

    onMount(loadGoogleMaps);
</script>

<html lang="en" data-theme="lemonade">
    <input
        type="text"
        id="autocomplete"
        placeholder={placeholder}
        class="input input-bordered w-full"
    />
</html>

<style>

</style>