#!/bin/bash
set -ex

GIT_REPO=${GIT_REPO}
GIT_REPO_FOLDER=${GIT_REPO_FOLDER:-odu}
GIT_SSHKEY=${GIT_SSHKEY}
GIT_PASSWORD=${GIT_PASSWORD}
LOCAL_TEST_FLAG=${LOCAL_TEST_FLAG:-""}

get_host() {
   # Examples of repos:
   # git@github.com:gerardo-garcia/gitops.git"
   repo=$1
   if echo "$repo" |grep -q "git"; then
       host="$repo"
       host=${host#git*@}
       host=${host%:*}
   else
       echo "Could not get the host from the repo"
       exit 1
   fi
   echo "$host"
}

REPO_FOLDER=${GIT_REPO_FOLDER}

if [ -n "${LOCAL_TEST_FLAG}" ]; then
    echo "Creating temporary folder for the repo"
    REPO_FOLDER=$(mktemp -t -d odu.XXXXXXXX)
fi

echo "Cloning Git repo ${GIT_REPO} into ${REPO_FOLDER}"
if [ -n "${GIT_SSHKEY}" ]; then
    if [ -z "${LOCAL_TEST_FLAG}" ]; then
        mkdir $HOME/.ssh
        echo "${GIT_SSHKEY}" | base64 -d > $HOME/.ssh/id_rsa
        GIT_HOST=$(get_host ${GIT_REPO})
	    ssh-keyscan ${GIT_HOST} >> $HOME/.ssh/known_hosts
        #echo "Host ${GIT_HOST}\n\tStrictHostKeyChecking no\n" >> $HOME/.ssh/config
        chmod 700 $HOME/.ssh/id_rsa
    fi
    git clone ${GIT_REPO} ${REPO_FOLDER}
elif [ -n "${GIT_PASSWORD}" ]; then
    sshpass -p ${GIT_PASSWORD} git clone ${GIT_REPO} ${REPO_FOLDER}
else
    git clone ${GIT_REPO} ${REPO_FOLDER}
fi

ls -la ${REPO_FOLDER}
ls -la ${REPO_FOLDER}/..
ls -la ${REPO_FOLDER}/../..

echo "DONE"

