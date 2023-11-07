<script lang="ts">
    import { Loader } from "@googlemaps/js-api-loader"

    export let API_KEY: string;
    export let map_data: any;

    let map: google.maps.Map;
    let container: HTMLElement;
    
    const loader = new Loader({
        apiKey: API_KEY,
        version: "weekly",
        libraries: ["geometry"]
    });

    loader.load().then(async () => {
        const { Map } = await google.maps.importLibrary("maps") as google.maps.MapsLibrary;
        map = new Map(container, {
            center: { lat: 37.7749, lng: -122.4194 },
            zoom: 8,
        });

        var encodedPolyline = map_data["polyline"];
        var decodedPath = google.maps.geometry.encoding.decodePath(encodedPolyline);
        var polyline = new google.maps.Polyline({
            path: decodedPath,
            geodesic: true,
            strokeColor: '#0000FF',
            strokeOpacity: 1.0,
            strokeWeight: 3
        });
        polyline.setMap(map);

        for(const leg of map_data.legs){
            new google.maps.Marker({
                position: {lat: leg.lat, lng: leg.lon},
                map,
                label: String(leg.sequence)
            });
        }

    //     new google.maps.Marker({ position: { lat: 37.3365145, lng: -121.88460509999999 }, map, label: "0" });
    //     new google.maps.Marker({ position: { lat: 37.3348697, lng: -121.89332780000001 }, map, label: "1" });
    //     new google.maps.Marker({ position: { lat: 37.3416232, lng: -121.89058250000001 }, map, label: "2" });
    //     new google.maps.Marker({ position: { lat: 38.074518999999995, lng: -122.706558 }, map, label: "3" });
    });

</script>




<style>
    .full-screen {
    width: 100vw;
    height: 40vh;
    }
</style>
    
<div class="full-screen" bind:this={container}></div>