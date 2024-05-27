#!/bin/bash

export GIT_REPO=${1:-${GIT_REPO}}
export GIT_SSHKEY=${2:-${GIT_SSHKEY}}
export GIT_REPO_FOLDER=${3:-${GIT_REPO_FOLDER}}
export GIT_PASSWORD=${GIT_PASSWORD}
LOCAL_TEST_FLAG=${LOCAL_TEST_FLAG:-""}

source $HOME/clone_git_repo.sh
