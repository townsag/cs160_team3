# cs160_team3
This is the shared repository for Team 3 of SJSU CS160. We are working on developing a grocery delivery application.

## User Guide
To run OGO follow these steps
1. git clone repository to directory
```
git clone https://github.com/townsag/cs160_team3.git
```
2. go into directory 
```
cd cs160_team3
```

3. add a file called .env and paste this into it with your API key/s instead
```
[KEYS]
GOOGLE_ROUTES_API_KEY=""
GOOGLE_PLACES_API_KEY=""
```
4. build Docker image (need to have Docker installed)
```
docker build . -t ogo
```
5. run the Docker file
```
docker run -p 3000:3000 ogo
```
6. go to localhost:3000 or your IP address and port 3000 to access on local network
steps are the same for both Windows Powershell(bat) and Linux/Mac (bash/zsh)

8. Google Drive link to view video description

[`[https://drive.google.com/file/d/1M_YosK72QE9pKzKjL-qJtcgV2PADwkhq/view](https://drive.google.com/file/d/1v6AWZsNofzVQYB1ZKNt5k8n1TzoMMGpR/view)`](https://drive.google.com/file/d/1v6AWZsNofzVQYB1ZKNt5k8n1TzoMMGpR/view)https://drive.google.com/file/d/1v6AWZsNofzVQYB1ZKNt5k8n1TzoMMGpR/view
