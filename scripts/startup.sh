#! /bin/bash

# This script creates the cluster from scratch and deploy everything
coffee=$(python3 -c 'print("\u2615")')

kind create cluster --config=./manifests/kind-config.yaml
sleep 10

# Deploy ollama
kubectl apply -f ./manifests/ollama/
sleep 10

# Wait for it to be ready
echo "Pulling the Ollama image and creating the pod"
kubectl wait --for=condition=Ready pod  --all --timeout=1200s

# Pull the model
echo "Pulling the model, it might take for a while (30 seconds depending on your internet speed)"
kubectl exec $(kubectl get pods -l app=ollama -o=jsonpath='{.items[0].metadata.name}') -- ollama pull llama3.2:1b

# Deploy the api
kubectl apply -f ./manifests/api/

# Pull the api
echo "Pulling the Yggdrasil API image, it might take for a while (7 minutes depending on your internet speed), Enjoy your coffee! $coffee"
kubectl wait --for=condition=Ready pod  --all --timeout=1200s

echo "You can now access Yggdrasil API via http://localhost:8080"
echo "To see the Yggdrasil API Docs, use http://localhost:8080/docs"
