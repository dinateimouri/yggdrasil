#! bash

# Delete ollama manifests
kubectl delete -f ./manifests/ollama
sleep 5

# Delete Kind cluster
kind delete cluster
