# minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-arm64
sudo install minikube-darwin-arm64 /usr/local/bin/minikube
minikube start
minikube kubectl -- get po -A
alias kubectl="minikube kubectl --"
alias k="minikube kubectl --"
minikube dashboard
minikube pause
minikube unpause
minikube stop
minikube config set memory 9001
minikube addons list
minikube delete --all

## minikube ingress
minikube addons enable ingress
minikube tunnel

# lens
brew install --cask lens

# helm cli
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm search hub wordpress
helm search repo brigade
helm install happy-panda bitnami/wordpress
helm status happy-panda
helm show values bitnami/wordpress
helm install -f values.yaml bitnami/wordpress --generate-name
helm install foo foo-0.1.1.tgz
helm install foo path/to/foo
helm install foo https://example.com/charts/foo-1.2.3.tgz
helm upgrade -f panda.yaml happy-panda bitnami/wordpress
helm get values happy-panda
helm rollback happy-panda 1
--timeout 5m0s
--wait
--no-hooks
(upgrade & rollback only) --recreate-pods
helm uninstall happy-panda
helm list
helm uninstall --keep-history
helm list --uninstalled
helm list --all
helm repo list
helm repo add dev https://example.com/dev-charts
helm repo update
helm repo remove
https://helm.sh/docs/topics/charts/
helm create my-chart
helm lint
helm package my-chart
helm install my-chart ./my-chart-0.1.0.tgz
https://helm.sh/docs/topics/chart_repository/
https://helm.sh/docs/howto/charts_tips_and_tricks/
[Sync Chart to Google Cloud Storage bucket](https://helm.sh/docs/howto/chart_repository_sync_example/)
[Sync Chart with GitHub Actions](https://helm.sh/docs/howto/chart_releaser_action/)
[FAQ](https://helm.sh/docs/faq/troubleshooting/)

# prometheus
https://www.containiq.com/post/kubernetes-monitoring-with-prometheus
https://github.com/prometheus-community/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace monitoring
helm install prometheus prometheus-community/prometheus --namespace monitoring
It picks up on the airflow chart automagically. Try searching for airflow_scheduler_heartbeat.
Access by port forwarding the prometheus-server Service

# grafana
https://github.com/grafana/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
grafana.yaml
```
adminPassword: admin
datasources:
  datasources.yaml:
    apiVersion: 1
    datasources:
    - name: Prometheus
      type: prometheus
      url: http://<prometheus-server>.<monitoring_namespace>.<svc.cluster.local>
      access: proxy
      isDefault: true
```
helm install grafana grafana/grafana \
--namespace monitoring \
--values grafana.yaml
[Grafana Template for k8s](https://grafana.com/grafana/dashboards/6417-kubernetes-cluster-prometheus/)
[Grafana Template for airflow](https://github.com/databand-ai/airflow-dashboards/tree/main/grafana)
Default user/pass is admin/admin
How to enable persistence on GKE?
--set persistence.storageClassName="default" \
--set persistence.enabled=true \
Should I set the service type?
--set service.type=LoadBalancer
How to load dashboards using the helm values file?
Access by port-forwarding the grafana Service
TODO: add Ingress for grafana

# airflow
https://airflow.apache.org/docs/helm-chart/stable/index.html
helm repo add apache-airflow https://airflow.apache.org
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace
helm upgrade ^ might take a while
```
Release "airflow" does not exist. Installing it now.
NAME: airflow
LAST DEPLOYED: Wed Jan 18 22:31:09 2023
NAMESPACE: airflow
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Thank you for installing Apache Airflow 2.4.1!

Your release is named airflow.
You can now access your dashboard(s) by executing the following command(s) and visiting the corresponding port at localhost in your browser:

Airflow Webserver:     kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow
Default Webserver (Airflow UI) Login credentials:
    username: admin
    password: admin
Default Postgres connection credentials:
    username: postgres
    password: postgres
    port: 5432

You can get Fernet Key value by running the following:

    echo Fernet Key: $(kubectl get secret --namespace airflow airflow-fernet-key -o jsonpath="{.data.fernet-key}" | base64 --decode)

###########################################################
#  WARNING: You should set a static webserver secret key  #
###########################################################

You are using a dynamically generated webserver secret key, which can lead to
unnecessary restarts of your Airflow components.

Information on how to set a static webserver secret key can be found here:
https://airflow.apache.org/docs/helm-chart/stable/production-guide.html#webserver-secret-key
```
helm ls -A
helm upgrade airflow apache-airflow/airflow --namespace airflow
helm delete airflow --namespace airflow
How to secure PostgreSQL?
Which executor is installed?
How to upload airflow image to repository for GKE? 
Access by port-forwarding the airflow-webserver Service, or by enabling ingress and running `minikube tunnel` then opening 127.0.0.1:80
How to persist logs? https://airflow.apache.org/docs/helm-chart/stable/manage-logs.html#manage-logs
https://airflow.apache.org/docs/helm-chart/stable/setting-resources-for-containers.html
https://airflow.apache.org/docs/helm-chart/stable/customizing-workers.html
https://airflow.apache.org/docs/helm-chart/stable/parameters-ref.html

## Build Airflow Docker and load into k8s
docker build --tag xs-airflow:0.0.1 .
airflow.yaml
```
images:
  airflow:
    repository: xs-airflow
    tag: 0.0.1
```
helm upgrade airflow apache-airflow/airflow --namespace airflow --values ../helm/airflow.yaml
`Failed to pull image "xs-airflow:0.0.1": rpc error: code = Unknown desc = Error response from daemon: pull access denied for xs-airflow, repository does not exist or may require 'docker login': denied: requested access to the resource is denied`
https://minikube.sigs.k8s.io/docs/handbook/pushing/
eval $(minikube docker-env)
Then build again.

## Set Webserver Secret Key
python3 -c 'import secrets; print(secrets.token_hex(16))'
webserverSecretKey: 93d993ce543dcd3d188021066b2d0b6e in values.yaml