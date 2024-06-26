# Welcome to my project!

### Project description

the heart of the project is a fastAPI application written in python.

the application tracks companies and the company's revenues with the user's input.

the application performs several actions in mongoDB database.

this project contains helm charts for both my application and jenkins.

the project also contains a kind-config.yaml to handle all of the port forwarding and host volumes.

every other chart needs to be deployed by using an helm install command.



### Home-Page Capture

<div align="center"><img src="/readme_images/loc.png" alt="fastapi" width="756.5" height="239"></div>

### Company-Info Capture

<div align="center"><img src="/readme_images/info.png" alt="fastapi" width="778" height="590"></div>


## charts

### FastApi
A FastAPI app that performs several actions in mongoDB database
<div align="center"><img src="/readme_images/fastapi.png" alt="fastapi" width="300" height="300"></div>

### MongoDB
A Database that contains company information and revenues in a json form 
<div align="center"><img src="/readme_images/mongo.png" alt="fastapi" width="300" height="300"></div>

### argoCD
Deploys the application and the jenkinsfile.
Use the argocd-config-and-deploy.yaml that specifies the argo applications.
<div align="center"><img src="/readme_images/argo.png" alt="argo" width="300" height="300"></div>

### promethues
Scrapes both the App pods and the MongoDB pods
<div align="center"><img src="/readme_images/prometheus.png" alt="mongo" width="300" height="300"></div>

### grafana
that needs the grafana-service.yaml to grant access from outside the cluster.
<div align="center"><img src="/readme_images/grafana.png" alt="grafana" width="300" height="300"></div>


## Commands:
- kind create cluster --name finalproject --config Final-Project/kind-config.yml
- helm install argocd argo/argo-cd --namespace argocd-namespace --create-namespace --set server.admin.enabled=true --set server.admin.password=argocd123 --set server.service.type=NodePort --set server.service.nodePorts.http=30080 --set persistence.enabled=true --set persistence.size=8Gi --set persistence.storageClass=standard
- kubectl apply -f .\Final-Project\argocd-config-and-deploy.yaml
- helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace
- helm install grafana grafana/grafana --namespace monitoring
- kubectl apply -f .\Final-Project\grafana-service.yaml


### kind create cluster --name finalproject --config Final-Project/kind-config.yml
creating the cluster and using the kind-config.yml to configure the cluster

### helm install argocd argo/argo-cd...
helm chart that runs argocd in a argocd-namespace namespace and allocates resources

### kubectl apply -f .\Final-Project\argocd-config-and-deploy.yaml
applies the argocd-config-and-deploy.yaml to specify the argocd applications fastapi and jenkins

### helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace
helm chart that runs prometheus in a monitoring namespace

### helm install grafana grafana/grafana --namespace monitoring
helm chart that runs grafana in the same namespace as promethues

### kubectl apply -f .\Final-Project\grafana-service.yaml
applies the grafana-service.yaml to configure a grafana service so the grafana can be exported via NodePort