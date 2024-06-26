# ODU container

## Build and test docker images

```bash
docker build -t osm-odu:latest .
source test-environment.rc
docker run --env GIT_REPO="${GIT_REPO}" --env GIT_SSHKEY="${GIT_SSHKEY}" --env GIT_MANIFEST_FOLDER="${GIT_MANIFEST_FOLDER}" -it osm-odu:latest
```

```bash
docker build -t osm-odu:latest .
docker tag osm-odu:latest gerardogarcia/osm-odu:latest
docker push gerardogarcia/osm-odu:latest
```

## Argo

### Installation

```bash
kubectl create namespace argo
kubectl apply -n argo -f https://github.com/argoproj/argo-workflows/releases/download/v3.4.11/install.yaml
# Switch the authentication mode to server so that we can bypass the UI login for now
kubectl patch deployment \
  argo-server \
  --namespace argo \
  --type='json' \
  -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/args", "value": [
  "server",
  "--auth-mode=server"
]}]'
# Port forward the UI
kubectl -n argo port-forward deployment/argo-server 2746:2746
```

To use the default authentication (client):

```bash
kubectl -n argo create role osm --verb=list,update --resource=workflows.argoproj.io
kubectl -n argo create sa osm
kubectl -n argo create rolebinding osm --role=osm --serviceaccount=argo:osm
kubectl -n argo apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: osm.service-account-token
  namespace: argo
  annotations:
    kubernetes.io/service-account.name: osm
type: kubernetes.io/service-account-token
EOF
ARGO_TOKEN="Bearer $(kubectl -n argo get secret osm.service-account-token -o=jsonpath='{.data.token}' | base64 --decode)"
echo $ARGO_TOKEN
```

### Special configuration of roles for ArgoWorkflows

In order to create configmaps and secrets, as part of an Argo Workflow, a role must exist with enough permissions to do it. If you are using argo-role, you can edit like this `kubectl -n argo edit role argo-role`:

```yaml
- apiGroups:
  - ""
  resources:
  - secrets
  - configmaps
  verbs:
  - create
  - get
  - update
```

## Usage

```bash
# Create a secret to store your SSH key to be used for git
GIT_SSHKEY_FILE="$HOME/.ssh/id_rsa"
kubectl -n argo create secret generic git-secret --from-file=id_rsa="${GIT_SSHKEY_FILE}"
GIT_USER_NAME="gerardo-garcia"
GIT_USER_EMAIL="gerardo-garcia@users.noreply.github.com"
kubectl -n argo create configmap git-config --from-literal=GIT_USER_NAME="${GIT_USER_NAME}" --from-literal=GIT_USER_EMAIL="${GIT_USER_EMAIL}"

# Upload templates
kubectl -n argo apply -f workflowtemplates

# List templates and workflows
kubectl -n argo get workflowtemplates
kubectl -n argo get workflows

# Run workflow not based on containers
kubectl -n argo create -f osm-workflow.yaml

# Run workflow based on containers
kubectl -n argo create -f osm-workflow-with-templates.yaml

# Check resources created by the workflows
kubectl -n argo get pv,pvc,configmaps,secrets
```
