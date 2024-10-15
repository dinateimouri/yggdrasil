#! bash

# Delete api manifests
kubectl delete -f ./manifests/api

# Delete ollama manifests
kubectl delete -f ./manifests/ollama
sleep 5

# Delete Kind cluster
kind delete cluster
