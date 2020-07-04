# WorldPathFinder

An API-wrapped pathfinder for navigating the World of Twelve

## Using the public API

The API is accessible at `alexisvialaret.fr/blackfalcon`

The only endpoint is `blackfalcon/get_path`

It supports the following keys as optional parameters:

```
start_map_id
end_map_id
start_cell_id
end_cell_id
```

### Example requests

To go from [6, -19] to [3, -18]

[Request](alexisvialaret.fr/blackfalcon/get_path?start_map_id=191106048;end_map_id=191102978):
`blackfalcon/get_path?start_map_id=191106048;end_map_id=191102978`

Result:
```JSON
[
    {"coord": "6;-19", "map_id": 191106048, "cell": 322, "direction": "w"}, 
    {"coord": "5;-19", "map_id": 191105024, "cell": 539, "direction": "s"}, 
    {"coord": "5;-18", "map_id": 191105026, "cell": 140, "direction": "w"}, 
    {"coord": "4;-18", "map_id": 191104002, "cell": 266, "direction": "w"}
]
```


To go from [3, -19] cell 456 to [3, -20] cell 412

[Request](blackfalcon/get_path?start_map_id=191102976;start_cell_id=456;end_map_id=188744706;end_cell_id=412):
`blackfalcon/get_path?start_map_id=191102976;start_cell_id=456;end_map_id=188744706;end_cell_id=412`

Result:
```JSON
[
    {"coord": "3;-19", "map_id": 191102976, "cell": 461, "direction": "e"}, 
    {"coord": "4;-19", "map_id": 191104000, "cell": 11, "direction": "n"}, 
    {"coord": "4;-20", "map_id": 188745218, "cell": 210, "direction": "w"}
]
```

Note: the pathfinder is going to be much faster when specifying start and/or end cells


### Throttling

The public API is made available to you for testing purposes. In order to not overload my servers and allow everyone to use the API, I'm limiting the frequency of calls you can make to one every 5 seconds per IP.

If you want to get serious about using the API and need to get rid of the throttling, you can get in touch with me so I can dedicate you some infra or you can set up your own with the instructions below.

### Known limitations

- Special map changes: does not considers as neighbours the maps that require using an activable to change maps. This may cause the pathfinder to go the long way around or to fail to find a path.
- worldmap changes: the pathfinder will be unable to find a path between maps on different worldmaps. It will also not include worldmap changes to create a path (it will not use tunnels)
- Continents outside amakna: they should work, but my bots are only running in Amakna, so you might encounter issues.

### Reporting issues and requesting features

Please do so using GitHub issues. If you're reporting a problem, make sure to include the request you made, and any additional info that might help troubleshooting.

Requested features will be added (or not) at my discretion as time allows.

## Deploying your own

### From the Docker image

Credentials to access the backend and logs are placed in shared volumes. You will need to create these directories on your machine in order to run the image.

```shell script
mkdir WorldPathFinder
cd WorldPathFinder
mkdir secrets
mkdir logs
```

Get the credentials:
```
wget -O secrets/credentials.json https://raw.githubusercontent.com/AlexisVLRT/WorldPathFinder/master/secrets/credentials.json?token=AGH6RAYDDLNIEYZBQW3Q7A27ACB46
```

Then just run the docker image:

```
docker run -d -v `pwd`/secrets:/app/secrets -v `pwd`/logs:/app/logs -p 80:80 ugdha/world_path_finder
```
### From the GitHub repo

```shell script
git clone https://github.com/AlexisVLRT/WorldPathFinder.git
cd WorldPathFinder
```

Requires python 3 to run, tested with python 3.8.

To run it in a virtual environment (recommended):
```shell script
python -m venv venv
source venv/bin/activate
```

Install the required dependencies:
```shell script
python -m pip install -r requirements
```

Start the API:
```shell script
python bin/main.py
```
