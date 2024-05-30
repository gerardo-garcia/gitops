#!/bin/bash
set -ex -o pipefail

GIT_REPO=${GIT_REPO}
GIT_REPO_FOLDER=${GIT_REPO_FOLDER:-odu}
GIT_SSHKEY=${GIT_SSHKEY}
GIT_PASSWORD=${GIT_PASSWORD}
LOCAL_TEST_FLAG=${LOCAL_TEST_FLAG:-""}

export HERE=$(dirname "$(readlink -f "$BASH_SOURCE")")
echo "Sourcing git functions"
source "${HERE}/library/git_functions.sh"

REPO_FOLDER=${GIT_REPO_FOLDER}

if [ -n "${LOCAL_TEST_FLAG}" ]; then
    echo "Creating temporary folder for the repo"
    REPO_FOLDER=$(mktemp -t -d odu.XXXXXXXX)
fi

# if [ -n "${GIT_SSHKEY}" ] || [ -d "$HOME/.ssh/" ] && [ -z "${LOCAL_TEST_FLAG}" ]; then
    # write_sshkey
    # GIT_HOST=$(get_host ${GIT_REPO})
    # ssh-keyscan ${GIT_HOST} >> $HOME/.ssh/known_hosts
# fi

echo "Cloning Git repo ${GIT_REPO} into ${REPO_FOLDER}"
if [ -n "${GIT_PASSWORD}" ]; then
    sshpass -p ${GIT_PASSWORD} git clone ${GIT_REPO} ${REPO_FOLDER}
elif [ -d "$HOME/.ssh/" ] || [ -n "${GIT_SSHKEY}" ]; then
    export GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
    git clone ${GIT_REPO} ${REPO_FOLDER}
else
    git clone ${GIT_REPO} ${REPO_FOLDER}
fi

echo "Listing files in the repo folder and parent folders"
ls -la ${REPO_FOLDER}
ls -la ${REPO_FOLDER}/..
ls -la ${REPO_FOLDER}/../..

echo "DONE"
