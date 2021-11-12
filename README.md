# Context:

This project is an example of implementation of Carbon Footprint Calculator and deployed on IBM Cloud.
It uses the functions previously created to score a week's consumption into a carbon footprint.
It also allows for the reading of a barcode to determine the origin of a product and compute the distance it travalled

Main features of the app:
* Deployed in couple of lines of code
* Able to calculate Carbon Footprint based on questionaire
* Integrates Barcode Scanner to define country of origin of products
# Structure:

The code is structured as follows:
* app.py contains the core functions of the app, including the configuration of the app, the necessary imports and the execution of the prediction
* app.yaml is the app configuration file necessary for the setup of the project 
* user_sql.py is the code used for initializing the database and record the user's info following the  sign-in
* requirements.txt displays the necessary libraries and packages to run this app
* templates/ contain the HTML templates used for the front of this project


To run the code locally:
    * `set FLASK_APP=app.py` 
    * `python -m app`

  
  
# Deploy to IBM Cloud Kubernetes Service

Follow these instructions to deploy this application to a Kubernetes cluster and connect it with a Cloudant database.

## Download

```bash
https://github.com/call-for-code-team-one/carbon-footprint-jvd.git
cd carbon_footprint_app-jvd
```

## Build Docker Image

1. Find your container registry **namespace** by running `ibmcloud cr namespaces`. If you don't have any, create one using `ibmcloud cr namespace-add <name>`
2. Identify your **Container Registry** by running `ibmcloud cr info` (Ex: registry.ng.bluemix.net)
3. Build and tag (`-t`)the docker image by running the command below replacing REGISTRY and NAMESPACE with he appropriate values.

   ```sh
   docker build . -t <REGISTRY>/<NAMESPACE>/myapp:v1.0.0
   ```
   Example: `docker build . -t registry.ng.bluemix.net/mynamespace/myapp:v1.0.0

4. Push the docker image to your Container Registry on IBM Cloud

   ```sh
   docker push <REGISTRY>/<NAMESPACE>/myapp:v1.0.0
   ```

## Deploy

#### Create a Kubernetes cluster

1. [Creating a Kubernetes cluster in IBM Cloud](https://console.bluemix.net/docs/containers/container_index.html#clusters).
2. Follow the instructions in the Access tab to set up your `kubectl` cli.

#### Create a Cloudant Database 

1. Go to the [Catalog](https://console.bluemix.net/catalog/) and create a new [Cloudant](https://console.bluemix.net/catalog/services/cloudant-nosql-db) database instance.

2. Choose `Legacy and IAM` for **Authentication**

3. Create new credentials under **Service Credentials** and copy value of the **url** field.

4. Create a Kubernetes secret with your Cloudant credentials (url, username and password).

```bash
kubectl create secret generic cloudant --from-literal=url=<URL> --from-literal=username=<USERNAME> --from-literal=password=<PASSWORD>
```
Example:
```bash
kubectl create secret generic cloudant --from-literal=url=https://myusername:passw0rdf@username-bluemix.cloudant.com  --from-literal=username=myusername --from-literal=password=passw0rd
```

#### Create the deployment

1. Replace `<REGISTRY>` and `<NAMESPACE>` with the appropriate values in `kubernetes/deployment.yaml`
2. Create a deployment:
  ```shell
  kubectl create -f kubernetes/deployment.yaml
  ```
- Expose the service using an External IP and Loadbalancer
  ```
  kubectl expose deployment carbon_footprint_app-jvd --type LoadBalancer --port 8000 --target-port 8000
  ```

### Access the application

Verify **STATUS** of pod is `RUNNING`

```shell
kubectl get pods -l app=carbon_footprint_app-jvd
```

**Standard (Paid) Cluster:**

1. Identify your LoadBalancer Ingress IP using `kubectl get service get-started-python`
2. Access your application at t `http://<EXTERNAL-IP>:8000/`


## Clean Up
```bash
kubectl delete deployment,service -l app=carbon_footprint_app-jvd
kubectl delete secret cloudant
```