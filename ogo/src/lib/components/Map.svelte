<script lang="ts">
    import { Loader } from "@googlemaps/js-api-loader"
  import { onMount } from "svelte";
    
    export let API_KEY: string;

    let map: google.maps.Map;
    let container: HTMLElement;
    let polyline: google.maps.Polyline | null = null;
    let markers: google.maps.Marker[] = [];
    let Map: typeof google.maps.Map
    // let googleMaps: typeof google.maps;

    // let GeometryLibrary: google.maps.GeometryLibrary;
    // let Polyline: typeof google.maps.Polyline;

    const loader = new Loader({
        apiKey: API_KEY,
        version: "weekly",
        libraries: ["geometry"]
    });

    export async function init_map(){
        console.log("entering init map");
        await loader.load();
        const MapsLibrary = await google.maps.importLibrary("maps") as google.maps.MapsLibrary;
        Map = MapsLibrary.Map;

        // GeometryLibrary = await google.maps.importLibrary("geometry") as google.maps.GeometryLibrary;
        // Polyline = MapsLibrary.Polyline;
        // console.log("finished loading polyline library");


        map = new Map(container, {
            center: { lat: 37.330120, lng: -121.877430 },
            zoom: 10,
        });
        console.log("leaving init map");
    }

    export async function add_polyline(encodedPolyline: string){
        console.log("inside add polyline");
        await loader.load();
        remove_polyline();
        // console.log("this is the polyline: ", encodedPolyline);
        console.log(google.maps);
        // var decodedPath = google.maps.geometry.encoding.decodePath(encodedPolyline);
        var decodedPath = google.maps.geometry.encoding.decodePath(encodedPolyline);
        // console.log("this is the decoded path: ", decodedPath);
        polyline = new google.maps.Polyline({
            path: decodedPath,
            geodesic: true,
            strokeColor: '#0000FF',
            strokeOpacity: 1.0,
            strokeWeight: 3
        });
        polyline.setMap(map);
        console.log("this is map: ", map);
        console.log("after set map in add polyline");
    }

    export function remove_polyline(){
        if (polyline) {
            polyline.setMap(null);
        }
    }

    export function add_markers(marker_data: {[key: string]: any}[]){
        console.log("adding markers");
        remove_markers();
        marker_data.forEach(marker => {
            markers.push(new google.maps.Marker({
                position: {lat: marker.lat, lng: marker.lon}, 
                map, 
                label:String(marker.sequence)}));
        });
    }

    export function remove_markers(){
        // first hide all active markers
        for (let i = 0; i < markers.length; i++) {
            markers[i].setMap(null);
        }
        markers = [];
    }

    // onMount(async ()=>{
    //     await init_map();}
    //     );

    // import { Loader } from "@googlemaps/js-api-loader"

    // export let API_KEY: string;
    // export let map_data: any;

    // let map: google.maps.Map;
    // let container: HTMLElement;
    
    // const loader = new Loader({
    //     apiKey: API_KEY,
    //     version: "weekly",
    //     libraries: ["geometry"]
    // });

    // loader.load().then(async () => {
    //     const { Map } = await google.maps.importLibrary("maps") as google.maps.MapsLibrary;
    //     map = new Map(container, {
    //         center: { lat: 37.7749, lng: -122.4194 },
    //         zoom: 9,
    //     });

    //     var encodedPolyline = map_data["polyline"];
    //     var decodedPath = google.maps.geometry.encoding.decodePath(encodedPolyline);
    //     var polyline = new google.maps.Polyline({
    //         path: decodedPath,
    //         geodesic: true,
    //         strokeColor: '#0000FF',
    //         strokeOpacity: 1.0,
    //         strokeWeight: 3
    //     });
    //     polyline.setMap(map);

    //     for(const leg of map_data.legs){
    //         new google.maps.Marker({
    //             position: {lat: leg.lat, lng: leg.lon},
    //             map,
    //             label: String(leg.sequence)
    //         });
    //     }
    // });

</script>




<style>
    .full-screen {
    width: 100vw;
    height: 40vh;
    }
</style>
    
<div class="full-screen" bind:this={container}></div>