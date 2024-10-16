#! bash

# Delete api manifests
kubectl delete -f ./manifests/api

# Delete ollama manifests
kubectl delete -f ./manifests/ollama
sleep 5

# Delete Kind cluster
kind delete cluster

smiley=$(python3 -c 'print("\u263A")')
echo "Have a nice day! See you soon! $smiley"
