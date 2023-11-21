# cs160_team3
This is the shared repository for Team 3 of SJSU CS160. We are working on developing a grocery delivery application

## User Guide
To run OGO follow these steps
1. git clone
```
git clone https://github.com/townsag/cs160_team3.git
```
2. go into directory 
```
cd cs160_team3.git
```

3. add a file called .env and paste this into it with your api key/s instead
```
[KEYS]
GOOGLE_ROUTES_API_KEY=""
GOOGLE_PLACES_API_KEY=""
```
4. build docker image (need to have docker installed)
```
docker build . -t ogo
```
5. run the docker file
```
docker run -p 3000:3000 ogo
```
6. go to localhost:3000 or your ip address and port 3000 to access on local network
Steps are  the same on both windows powershell(bat) and linux/mac (bash/zsh)

7. Google Drive Link to View Video Description

[`[https://drive.google.com/file/d/1M_YosK72QE9pKzKjL-qJtcgV2PADwkhq/view](https://drive.google.com/file/d/1v6AWZsNofzVQYB1ZKNt5k8n1TzoMMGpR/view)`](https://drive.google.com/file/d/1v6AWZsNofzVQYB1ZKNt5k8n1TzoMMGpR/view)https://drive.google.com/file/d/1v6AWZsNofzVQYB1ZKNt5k8n1TzoMMGpR/view
