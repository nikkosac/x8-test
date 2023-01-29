This is a customization of the Apache Airflow Docker image

# Build
```
docker build --tag xs-airflow:0.0.1 .
```

# Push to minikube
```
eval $(minikube docker-env)
Then build
```