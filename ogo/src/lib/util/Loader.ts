import { Loader } from "@googlemaps/js-api-loader";

// let API_KEY: string;

// async function get_api_key() {
//     try {
//         const api_key_response = await fetch("/getMapConstants");
//         if (api_key_response.ok) {
//             const data = await api_key_response.json();
//             return data.API_KEY;
//         }
//     } catch (error) {
//         console.log("error: ", error);
//     }
// }

// async function initializeLoader() {
//     if (!API_KEY) {
//         API_KEY = await get_api_key();
//     }

//     return new Loader({
//         apiKey: API_KEY,
//         version: "weekly",
//         libraries: ["geometry", "places"],
//         region: "US"
//     });
// }

// const singleton_loader_promise = initializeLoader();

// export default singleton_loader_promise;


let apiKeyPromise: any;

export async function loadGoogleMaps() {
  if (!apiKeyPromise) {
    apiKeyPromise = fetch("/getPlacesConstants")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch API key");
        }
        return response.json();
      })
      .then((data) => {
        if (!data.API_KEY) {
          throw new Error("API key not found in response");
        }
        const loader = new Loader({
            apiKey: data.API_KEY,
            version: "weekly",
            libraries: ["geometry", "places"],
            region: "US"
        });
        return loader.load();
      });
  }
  return apiKeyPromise;
}