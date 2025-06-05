# Télecharger openfaas

helm repo add openfaas https://openfaas.github.io/faas-netes/
helm repo update

# Créer les namespaces

kubectl create namespace openfaas
kubectl create namespace openfaas-fn

# Générer un mot de passe pour l'interface OpenFaaS

PASSWORD=$(head -c 12 /dev/urandom | shasum| cut -d' ' -f1)
echo $PASSWORD > openfaas-password.txt
echo "Mot de passe OpenFaaS: $PASSWORD"

# Créer le secret pour l'authentification

kubectl -n openfaas create secret generic basic-auth \
 --from-literal=basic-auth-user=admin \
 --from-literal=basic-auth-password="$PASSWORD"

# Installer OpenFaaS

helm upgrade openfaas --install openfaas/openfaas \
 --namespace openfaas \
 --set functionNamespace=openfaas-fn \
 --set generateBasicAuth=false

# Configurer faas-cli

export OPENFAAS_URL=http://127.0.0.1:8080
echo -n "$PASSWORD" | faas-cli login --username admin --password-stdin

# Créer un déploiement Redis simple

kubectl create deployment redis --image=redis:alpine
kubectl expose deployment redis --port=6379 --name=redis-service

# Build et déploiement de get-quote

faas-cli build -f get-quote.yaml
faas-cli deploy -f get-quote.yaml

# Build et déploiement de save-feedback

faas-cli build -f save-feedback.yaml
faas-cli deploy -f save-feedback.yaml

# Accéder a Prometheus

kubectl port-forward -n openfaas svc/prometheus 9090:9090 &

## Requêtes Prometheus utiles

# Nombre total d'invocations par fonction

sum(gateway_function_invocation_total) by (function_name)

# Requêtes par seconde

rate(gateway_function_invocation_total[1m])

# Invocations des dernières 5 minutes

increase(gateway_function_invocation_total[5m])

![Screenshot of faas-cli list](/screenshots/faas-cli_list.png)

![Screenshot of curls](/screenshots/curl.png)

![Screenshot of openfaas console](/screenshots/openfaas.png)

![Screenshot of prometheus console](/screenshots/prometheus.png)
