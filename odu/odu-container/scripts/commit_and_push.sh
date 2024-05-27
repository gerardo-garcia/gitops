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

# git add 
# git commit
# git push
echo "DONE"

