# MTGCollection - API

## Conda

When using Python it is important to use a virtual environment. We use conda for this purpose. To use conda, first install [Anaconda](https://www.anaconda.com/) or [Miniconda](https://conda.io/miniconda.html).

Then, to create a conda environment, you have to use the command:

```sh
conda env create -f environment.yml
```

To activate the environment, use the following command:

```sh
conda activate mtg-api
```

Finally, to add kernel to Jupyter, you have to use `ipykernel` as follow:

```sh
python -m ipykernel install --user --name mtg-api --display-name "Python (mtg-api)"
```

### Reference

- [Anaconda](https://www.anaconda.com/)
- [Miniconda](https://conda.io/miniconda.html)

## FastAPI

[FastAPI](https://fastapi.tiangolo.com/) is a framework to build an APIs using Python.

### How to run the API?

```sh
uvicorn main:app --reload --log-level info
```

### Reference

- [FastAPI documentation](https://fastapi.tiangolo.com/)

## Docker
We utilize Docker for building an image and deploying it in Azure.

### Creating the Docker Image

To create a Docker image, follow these steps:

1. Open a terminal or command prompt and navigate to the root folder of the project where the Dockerfile is located.
2. Run the following command:

```sh
docker build -t mtg-api .
docker buildx build --platform linux/amd64 -t mtg-api:v1.0.3 .
```

This command builds the Docker image using the specified Dockerfile and tags it with the name `mtg-api`.

### Running the Docker Image

To run the Docker image, execute the following command:

```sh
docker run -p 80:80 mtg-api
```

This command starts a Docker container using the `mtg-api` image. The `-p 80:80` option maps port 80 of the host machine to port 80 of the container, enabling access to the application through port 80 on the host. Adjust the port mapping as needed based on your application's requirements.

Once the container is running, you can access the application by opening a web browser and navigating to `http://localhost`.

### How to deploy a Docker Image in Azure?

To deploy this application in Azure, you have to create an Azure Container Registry and a Web App for Containers. Then, you have to create Docker Image and push it to Azure Container Registry.

#### Login

The recommended method when working in a command line is with the Azure CLI command az acr login. For example, to log in to a registry named myregistry, log into the Azure CLI and then authenticate to your registry:

```sh
az login
az acr login --name myregistry
```
 
#### Create alias for the image

Use docker tag to create an alias of the image with the fully qualified path to your registry. This example specifies the samples namespace to avoid clutter in the root of the registry.

```sh
docker tag <local_image_name>:tag myregistry.azurecr.io/samples/<image_name>:tag

```

#### Push the Docker Image to ACR

Now that you've tagged the image with the fully qualified path to your private registry, you can push it to the registry with docker push:

```sh
docker push myregistry.azurecr.io/samples/<image_name>:tag
```


### Reference
- [Push Docker Image to ACR](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-docker-cli)

