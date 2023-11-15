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

        markers.push(new google.maps.Marker({
            position: { lat: 37.330120, lng: -121.877430 },
            map,
            label: "S"
        }));

        marker_data.forEach(marker => {
            const marker_obj = new google.maps.Marker({
                position: {lat: marker.lat, lng: marker.lon}, 
                map, 
                label:String(marker.sequence + 1)
            });

            const infowindow = new google.maps.InfoWindow({
                content: `<p>Username: ${marker.username}</p><p>Order Number: ${marker.order_id}</p>`,
                ariaLabel: "infoWindow",
            });

            marker_obj.addListener("click", () => {
                infowindow.open({
                anchor: marker_obj,
                map,
                });
            });

            markers.push(marker_obj);
        });
    }

    export function remove_markers(){
        // first hide all active markers
        for (let i = 0; i < markers.length; i++) {
            markers[i].setMap(null);
        }
        markers = [];
    }
</script>




<style>
    .full-screen {
    width: 100vw;
    height: 40vh;
    }
</style>
    
<div class="full-screen" bind:this={container}></div>
