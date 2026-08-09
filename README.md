# Lab 1 — Docker Fundamentals: Flask Application Containerization

## Project Overview

This lab demonstrates the core Docker workflow by containerizing a Python Flask web application.

The application is packaged into a Docker image using a `Dockerfile`, then launched as a running Docker container. The container exposes the Flask application on port `5000`, while Docker maps it to a host port for external access.

### Core Architecture

```text
Developer
   |
   | writes
   v
Dockerfile
   |
   | docker build
   v
Docker Image
   |
   | docker run
   v
Docker Container
   |
   | runs
   v
Flask Application
   |
   | listens
   v
Container Port 5000
   |
   | -p 5000:5000
   v
Host Port 5000
   |
   v
Browser / curl
```

# 1. Aim

To containerize a Python Flask web application using Docker and understand the complete lifecycle from application source code to a running container.

# 2. Objectives

By completing this lab, I learned how to:

* Create a Dockerfile.
* Select a base image.
* Define a container working directory.
* Copy application dependencies into an image.
* Install Python dependencies during image build time.
* Copy application source code into the image.
* Define the container startup command.
* Build a Docker image.
* Run a container from an image.
* Map host ports to container ports.
* Understand Docker bridge networking.
* Test a containerized application using `curl`.
* Inspect a running container using `docker inspect`.
* Understand the difference between build time and runtime.
* Understand the difference between an image and a container.


# 3. Application Architecture

```text
Host Machine
     |
     | Host Port 5000
     v
Docker Engine
     |
     | Port Mapping
     | 5000:5000
     v
Docker Container
     |
     | Container Port 5000
     v
Flask Application
     |
     v
Python Runtime
```

The Flask application listens on:

```text
0.0.0.0:5000
```

Docker maps:

```text
Host:5000  --->  Container:5000
```

Therefore, the application can be accessed through:

```text
http://localhost:5000
```


# 4. Project Structure

```text
valarie-docker-app/
├── Dockerfile
├── app.py
├── requirements.txt
└── .dockerignore
```

### `app.py`

The Flask application contains the application logic and starts the Flask web server.

### `requirements.txt`

Contains external Python dependencies required by the application.

Example:

```text
flask
```

Docker uses this file during the image-building process so that the application's dependencies are installed inside the image.


# 5. Dockerfile

```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]

EXPOSE 5000
```


# 6. Dockerfile Breakdown

## FROM

```dockerfile
FROM python:3.12
```

Defines the base image.

The Python image provides the Python runtime and required operating-system components needed to run the application.

### Cloud engineering analogy

The base image is similar to selecting a foundational machine image such as an AWS AMI.


## WORKDIR

```dockerfile
WORKDIR /app
```

Creates/selects `/app` as the working directory inside the image.

Subsequent commands operate relative to this directory.


## COPY requirements.txt

```dockerfile
COPY requirements.txt .
```

Copies the dependency file from the build context into `/app` inside the image.

The `.` means the current working directory, which is `/app`.


## RUN

```dockerfile
RUN pip install -r requirements.txt
```

Installs Flask and other dependencies.

### Important concept

`RUN` executes during **image build time**.

It becomes part of the resulting image.

```text
docker build
      |
      v
Dockerfile
      |
      v
RUN commands execute
      |
      v
Docker Image
```


## COPY app.py

```dockerfile
COPY app.py .
```

Copies the Flask application into the image.



## CMD

```dockerfile
CMD ["python", "app.py"]
```

Defines the default command that runs when the container starts.

### Important concept

`CMD` is associated with **container runtime**.

```text
Docker Image
      |
      | docker run
      v
Container starts
      |
      v
CMD executes
      |
      v
python app.py
      |
      v
Flask application runs
```


# 7. RUN vs CMD

This is one of the most important Docker concepts from this lab.

| Instruction | Purpose                     | When it happens   |
| ----------- | --------------------------- | ----------------- |
| `RUN`       | Builds/configures the image | Build time        |
| `CMD`       | Starts the application      | Container runtime |

### Interview answer

> `RUN` executes while the Docker image is being built and its result becomes part of the image. `CMD` defines the default process that runs when a container is started from that image.


# 8. EXPOSE

```dockerfile
EXPOSE 5000
```

Documents that the application listens on container port `5000`.

### Important distinction

`EXPOSE` does **not** publish the port to the host by itself.

Actual host-to-container connectivity is created with:

```bash
-p 5000:5000
```

# 9. Building the Docker Image

Command used:

```bash
docker build -t valarie-cloud-app:v1 .
```

### Meaning

```text
docker build
```

Builds an image.

```text
-t valarie-cloud-app:v1
```

Assigns the image name and tag.

```text
.
```

Specifies the current directory as the Docker build context.

### Build workflow

```text
Dockerfile
requirements.txt
app.py
      |
      v
docker build
      |
      v
Python 3.12 base image
      |
      v
Install dependencies
      |
      v
Copy application
      |
      v
Docker Image
```

The build completed successfully.


# 10. Running the Container

The container was launched with port mapping:

```bash
docker run -d \
  --name valarie-cloud-container \
  -p 5000:5000 \
  valarie-cloud-app:v1
```

### Port mapping

```text
-p HOST_PORT:CONTAINER_PORT
```

Therefore:

```text
5000:5000
```

means:

```text
Host port 5000
       |
       v
Container port 5000
       |
       v
Flask application
```


# 11. Container Verification

Command:

```bash
docker ps
```

The container showed:

```text
0.0.0.0:5000->5000/tcp
```

This confirms that Docker published host port `5000` to container port `5000`.



# 12. Application Testing

The application was tested with:

```bash
curl http://localhost:5000
```

Result:

```text
Valarie Cloud Engineer Docker App
```

This confirmed that:

* The container was running.
* Flask was running.
* Flask was listening on port `5000`.
* Docker port mapping was functioning.
* The host could communicate with the containerized application.


# 13. Understanding 0.0.0.0

The Flask application listens on:

```text
0.0.0.0:5000
```

`0.0.0.0` means Flask listens on all network interfaces available to the container.

This allows Docker networking and published port mapping to reach the application.

It should not be interpreted as the Docker host itself.



# 14. Docker Bridge Networking

The container was running on Docker's default bridge network.

The container received its own internal IP address.

Example:

```text
Container
   |
   | bridge network
   v
172.17.x.x
```

The Docker bridge network provides connectivity between the container and Docker's networking environment.

Port publishing provides access from the host into the container.



# 15. Docker Inspect

The running container was inspected using:

```bash
docker inspect valarie-cloud-container
''

Important information observed included:
 
NetworkMode: bridge
WorkingDir: /app
Cmd: python app.py
ExposedPorts: 5000/tcp
HostPort: 5000
ContainerPort: 5000
Container IP: 172.17.0.4
Gateway: 172.17.0.1

This demonstrated that Docker stores the container's configuration, networking, command, image reference, and port mappings.


# 16. Image vs Container

## Docker Image

A Docker image is the reusable template/blueprint containing:

* Application code
* Dependencies
* Runtime
* Filesystem layers
* Configuration instructions

## Docker Container

A container is a running instance created from an image.


Docker Image
     |
     | docker run
     v
Docker Container


One image can be used to create multiple containers.


# 17. Docker Image Lifecycle

Developer
    |
    v
Dockerfile
    |
    v
docker build
    |
    v
Docker Image
    |
    | docker run
    v
Docker Container
    |
    v
Application

# 18. Dockerfile vs Docker Compose

Dockerfile and Docker Compose have different responsibilities.

### Dockerfile

Defines **how to build one application image**.


Dockerfile
    |
    v
Docker Image
    |
    v
Container
```

### Docker Compose

Defines **how multiple services should work together**.


docker-compose.yml
       |
       +---- Web service
       |
       +---- Database service
       |
       +---- Network
       |
       +---- Volumes
       |
       +---- Environment variables


Docker Compose is therefore more concerned with **application orchestration at the local/container level**, while the Dockerfile defines the image itself.


# 19. Key Lessons Learned

### Lesson 1

An image is not a running application.

It is the reusable package used to create containers.

### Lesson 2

A container is an isolated runtime environment created from an image.

### Lesson 3

`RUN` happens during image construction.

### Lesson 4

`CMD` runs when the container starts.

### Lesson 5

`EXPOSE` documents the intended container port but does not publish it.

### Lesson 6

`-p 5000:5000` creates host-to-container port mapping.

### Lesson 7

`0.0.0.0` allows the Flask application to listen on all container network interfaces.

### Lesson 8

Containers are ephemeral, but persistent data can be handled separately using volumes or external services such as Amazon RDS.


# 20. Final Architecture

                         DEVELOPER
                             |
                             |
                       Dockerfile
                             |
                             | docker build
                             v
                    +------------------+
                    |   Docker Image   |
                    | valarie-cloud-   |
                    |     app:v1       |
                    +------------------+
                             |
                             | docker run
                             v
                  +-----------------------+
                  |    Docker Container   |
                  |                       |
                  |   Python 3.12         |
                  |   /app                |
                  |   app.py              |
                  |                       |
                  |   Flask :5000         |
                  +-----------------------+
                             |
                             |
                    Docker Bridge Network
                             |
                             v
                    Host Port :5000
                             |
                     +-------+-------+
                     |               |
                   curl           Browser
                     |               |
                     +-------+-------+
                             |
                             v
                  Valarie Cloud Engineer
                         Docker App

# 22. Lab Result

The Flask application was successfully containerized and deployed using Docker.

The final workflow was successfully demonstrated:


Application
     ↓
Dockerfile
     ↓
Docker Build
     ↓
Docker Image
     ↓
Docker Run
     ↓
Docker Container
     ↓
Port Mapping
     ↓
Host
     ↓
curl / Browser
     ↓
Application Response


**Lab 1 Status: COMPLETE ✅**

