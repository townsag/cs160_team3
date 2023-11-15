<script  lang="ts">
    import { onMount } from "svelte";
    import { Loader } from "@googlemaps/js-api-loader";
    import { fetchApiKey } from "../util/RequestController";
    import { alert } from '../stores/alertStore';
    import AlertDaisy from "./AlertDaisy.svelte";

    export let placeholder: string;
    export let onPlaceSelect: ((place: any) => void) | undefined;

    async function loadGoogleMaps() {
        try {
            const result = await fetchApiKey();
        
            const loader = new Loader({
                apiKey: result.API_KEY,
                version: "weekly",
                libraries: ["places"],
                region: "US"
            });

            await loader.importLibrary("places");
            initAutocomplete();
        } catch (error) {
            console.error("Error loading Google Maps API:", error);
        }
    };

    const initAutocomplete = () => {
        const input = document.getElementById("autocomplete") as HTMLInputElement;

        // set bounding box around San Jose
        const sanJoseBounds = new google.maps.LatLngBounds(
            new google.maps.LatLng(37.1982, -122.1731), // southwest corner
            new google.maps.LatLng(37.4323, -121.7681)  // northeast corner
        );

        const autocomplete = new google.maps.places.Autocomplete(input, {
            types: ["address"],
            componentRestrictions: {"country": ["US"]},
            bounds: sanJoseBounds
        });

        autocomplete.addListener("place_changed", () => {
            const place = autocomplete.getPlace();

            // check if the selected place has geometry and is within the specified bounds
            if (place.address_components && place.geometry && place.geometry.location) {
                const placeLatLng = place.geometry.location;

                // check if the selected place has "San Jose" and "CA" in its address components
                var isSanJoseCA = place.address_components.some(function(component) {
                    return component.long_name === 'San Jose' && component.short_name === 'CA';
                });

                if (isSanJoseCA && sanJoseBounds.contains(placeLatLng)) {
                    console.log("Selected place:", place.formatted_address);
                    if (onPlaceSelect) {
                        onPlaceSelect(place.formatted_address);
                    }
                } else {
                    console.log("Selected place outside bounds. Ignoring.");
                    alert.set({ show: true, message: 'Error updating address: ' + "Selected address is outside of bounds", type: 'error'});
                    input.value = ""; // reset the input field
                }
            } else {
                console.log("Selected place has no valid geometry. Ignoring.");
                alert.set({ show: true, message: 'Error updating address: ' + "Selected address has no valid geometry", type: 'error'});
                input.value = ""; // reset the input field
            }
        });
    };

    onMount(async() => {
        await loadGoogleMaps();
    });
</script>

<html lang="en" data-theme="lemonade">
    <AlertDaisy {alert} />

    <input
        type="text"
        id="autocomplete"
        placeholder={placeholder}
        class="input input-bordered w-full"
    />
</html>

<style>

</style>