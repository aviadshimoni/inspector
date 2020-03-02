

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

Don't forget to edit the status page based on your needs and to comment out the unncessery  (in my lab I got 13 components, 1 for the all S3 Object Storage Service, and each 6 for PUT/GET Performance based on Object Size (cat config.py to see all Object Sizes tested in the script)

For production purposes, 4 prouduction services should be up:
* S3 Service (a storage backend provides native S3 API)
* Redis Service - don't forget to write redis hostname/ip in config.py file
* Cachet Status Page - containerized / daemonized - don't forget to write cachet host & cachet token api used for api calls

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














