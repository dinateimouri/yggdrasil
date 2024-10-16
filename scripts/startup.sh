#! bash

# This script creates the cluster from scratch and deploy everything
coffee=$(python3 -c 'print("\u2615")')

kind create cluster --config=./manifests/kind-config.yaml
sleep 5

# Deploy ollama
kubectl apply -f ./manifests/ollama/
sleep 5

# Wait for it to be ready
echo "Pulling the Ollama image and creating the pod"
kubectl wait --for=condition=Ready pod  --all --timeout=300s

# Pull the model
echo "Pulling the model, it might take 30 seconds"
kubectl exec $(kubectl get pods -l app=ollama -o=jsonpath='{.items[0].metadata.name}') -- ollama pull llama3.2:1b

# Deploy the api
kubectl apply -f ./manifests/api/

# Pull the api
echo "Pulling the Yggdrasil API image, it might take 7 minutes, Enjoy your coffee! $coffee"
kubectl wait --for=condition=Ready pod  --all --timeout=600s

echo "You can now access Yggdrasil API via http://localhost:8080"
echo "To see the Yggdrasil API Docs, use http://localhost:8080/docs"
