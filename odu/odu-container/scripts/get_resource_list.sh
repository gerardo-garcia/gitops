#!/bin/bash

export RESOURCE_FOLDER=${1:-${RESOURCE_FOLDER}}
export GIT_REPO_FOLDER=${2:-"/app/repos/osm-gitops-operations"}

RESOURCE_FOLDER=${RESOURCE_FOLDER}
kustomize cfg cat ${GIT_REPO_FOLDER}/${RESOURCE_FOLDER} --wrap-kind ResourceList --wrap-version config,kubernetes.io/v1alpha1


