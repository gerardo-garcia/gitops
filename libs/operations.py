import logging
from uuid import uuid4

logger = logging.getLogger("gitops")


def createClusterOperation(which, params):
    operation = {
        "id": str(uuid4()),
        "op": "create",  # create, update, delete
        "what": "cluster",  # it is only an example
        "which": which,
        "patch": [
            {"op": "replace", "path": "/metadata/name", "value": params["name"]},
            {"op": "replace", "path": "/spec/forProvider/dnsPrefix", "value": f"pref-{params['name']}"},
            {"op": "replace", "path": "/spec/publishConnectionDetailsTo/name", "value": f"kubeconfig-{params['name']}"},
            {"op": "replace", "path": "/spec/writeConnectionSecretToRef/name", "value": f"kubeconfig-{params['name']}"},
            {"op": "replace", "path": "/spec/forProvider/location", "value": params["cluster_location"]},
            {"op": "replace", "path": "/spec/forProvider/resourceGroupName", "value": params["resource_group"]},
            {"op": "replace", "path": "/spec/forProvider/kubernetesVersion", "value": params["k8s_version"]},
            {"op": "replace", "path": "/spec/forProvider/defaultNodePool/0/nodeCount", "value": params["node_count"]},
            {"op": "replace", "path": "/spec/forProvider/defaultNodePool/0/vmSize", "value": params["node_size"]},
        ],
    }
    return operation


def scaleClusterOperation(which, params):
    operation = {
        "id": str(uuid4()),
        "op": "update",  # create, update, delete
        "what": "cluster",  # it is only an example
        "which": which,
        "patch": [
            {"op": "replace", "path": "/spec/forProvider/defaultNodePool/0/nodeCount", "value": params["node_count"]},
        ],
    }
    return operation


def deleteClusterOperation(which):
    operation = {
        "id": str(uuid4()),
        "op": "delete",  # create, update, delete
        "what": "cluster",  # it is only an example
        "which": which,
    }
    return operation
