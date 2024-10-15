#! bash

kind create cluster --config=./manifests/kind-config.yaml
sleep 5

# Deploy ollama
kubectl apply -f ./manifests/ollama/
sleep 5

# Wait for it to be ready
echo "Pulling the Ollama image and creating the pod"
kubectl wait --for=condition=Ready pod  --all --timeout=300s

# Pull the model
echo "Pulling the model"
kubectl exec $(kubectl get pods -l app=ollama -o=jsonpath='{.items[0].metadata.name}') -- ollama pull llama3.2:1b

# Deploy the api
kubectl apply -f ./manifests/api/
