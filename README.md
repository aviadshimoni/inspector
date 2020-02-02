

Script used for S3 validation & benchmarking. Results will be shown on a Cachet Status Page.

## Getting Started

All you need is basic linux skills.

### Prerequisites

For testing purposes, deploy a ceph-nano container and run the docker-compose inside the inspector_build.

Before you get started, 4 containers should be up:
* ceph-nano (save the endpoint, access-key and secret-key)
* postgres used for Cachet data
* Cachet (a docker image built on top of nginx image) - for more info google Cachet-Docker
* Redis - used for inspector data

Dont forget to edit the status page based on your needs (in my lab component 1 is S3 Service, component 2 is Put Performance and component 3 is Get Performance.
### Installing

Clone the repository using git clone and edit the config.py (more instructions will be there)

### Deployment

Build the container:

```
docker build .
```

Run the container:

```
docker run <containerid>
```

Now results should be shown in the cachet status page.

## Authors

* Aviad Shimoni














