#!/bin/bash
set -ex -o pipefail

export GIT_REPO=${1:-${GIT_REPO}}
export GIT_SSHKEY=${2:-${GIT_SSHKEY}}
export GIT_MANIFEST_FOLDER=${3:-${GIT_MANIFEST_FOLDER}}
export GIT_PASSWORD=${GIT_PASSWORD}
LOCAL_TEST_FLAG=${LOCAL_TEST_FLAG:-""}

source $HOME/scripts/clone_git_repo.sh

GIT_MANIFEST_FOLDER=${GIT_MANIFEST_FOLDER}
kustomize cfg cat ${REPO_FOLDER}/${GIT_MANIFEST_FOLDER} --wrap-kind ResourceList --wrap-version config,kubernetes.io/v1alpha1
