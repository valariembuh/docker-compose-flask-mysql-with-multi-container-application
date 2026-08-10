# Docker Compose – Flask + MySQL Multi-Container Application

## Project Overview

Built a multi-container application using Docker Compose with:

* Flask web application
* MySQL database
* Docker named volume for persistent database storage
* Docker Compose networking and service-name DNS
* Container restart policies
* Docker Hub image deployment

## Architecture

```text
User
  |
  | localhost:5001
  v
Flask Container
  |
  | db:3306
  v
MySQL Container
  |
  v
Named Docker Volume
  |
  v
Persistent Database Data
```

## What I Built

Docker Compose manages two services:

* **web** — Flask application built from the Dockerfile
* **db** — MySQL 8.0 container pulled from Docker Hub

The services communicate over the Compose-created network using the DNS name `db` instead of a hard-coded IP address.

## Key Concepts Demonstrated

* Docker Compose multi-container orchestration
* Dockerfile image building
* Image vs. container lifecycle
* Host-to-container port mapping
* Docker service-name DNS
* `depends_on`
* Restart policies
* Named Docker volumes
* Database persistence
* Container replacement and recovery
* Docker Hub push and pull

## Persistence Test

A database table was created with test data:

```text
Valarie Docker Persistence Test
```

The MySQL container was then removed while the named Docker volume was preserved.

A new MySQL container was created using the same volume.

The original database table and data were successfully recovered.

**Result: Persistence test PASSED.**

## Run the Application

```bash
docker compose up -d --build
```

Check the services:

```bash
docker compose ps
```

Test the Flask application:

```bash
curl localhost:5001
```

Test Flask-to-MySQL connectivity:

```bash
curl localhost:5001/db
```

Expected result:

```text
Database connection: SUCCESS
```

## Docker Hub

Docker image:

```text
docker.io/valariembuh/valarie-docker-app:v1
```

The image was pushed to Docker Hub, removed locally, pulled again from Docker Hub, and successfully run as a new container.

## Evidence

Screenshots documenting the lab are available in:

```text
screenshots/
```

Key evidence includes:

* Compose services running
* Flask-to-MySQL connectivity
* Database persistence before container deletion
* Database container removal with volume preserved
* Database persistence successfully recovered

## Result

**Lab 2 completed successfully.**

This lab demonstrates practical Docker Compose, multi-container networking, persistent storage, service dependencies, failure recovery, and Docker Hub image deployment.

