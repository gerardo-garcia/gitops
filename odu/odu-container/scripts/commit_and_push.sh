#!/bin/bash
set -ex -o pipefail

GIT_REPO_FOLDER=${GIT_REPO_FOLDER:-odu}
GIT_BRANCH=${GIT_BRANCH:-test}
RESOURCE_FOLDER=${RESOURCE_FOLDER:-}
GIT_SSHKEY=${GIT_SSHKEY:-}
GIT_PASSWORD=${GIT_PASSWORD:-}
GIT_MAIN_BRANCH=${GIT_MAIN_BRANCH:-"main"}
COMMIT_MESSAGE=${COMMIT_MESSAGE:-"Commit message"}

export HERE=$(dirname "$(readlink -f "$BASH_SOURCE")")
echo "Sourcing git functions"
source "${HERE}/library/git_functions.sh"

pushd "${GIT_REPO_FOLDER}"

config_local_git_user_email

echo "Creating branch into ${REPO_FOLDER}"
git checkout -b ${GIT_BRANCH}

echo "Creating commit"
git status
git add ${RESOURCE_FOLDER}
git status
git commit -m "Operation ${GIT_BRANCH}: ${COMMIT_MESSAGE}"
git status

echo "Merge branch ${GIT_BRANCH} onto ${GIT_MAIN_BRANCH}"
git checkout ${GIT_MAIN_BRANCH}

echo "Pulling Git repo"
if [ -n "${GIT_PASSWORD}" ]; then
    sshpass -p ${GIT_PASSWORD} git pull
elif [ -d "$HOME/.ssh/" ] || [ -n "${GIT_SSHKEY}" ]; then
    export GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
    git pull
else
    git pull
fi

git merge --no-ff ${GIT_BRANCH}

echo "Push"
if [ -n "${GIT_PASSWORD}" ]; then
    sshpass -p ${GIT_PASSWORD} git push origin ${GIT_MAIN_BRANCH}
elif [ -d "$HOME/.ssh/" ] || [ -n "${GIT_SSHKEY}" ]; then
    export GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
    git push origin ${GIT_MAIN_BRANCH}
else
    git push origin ${GIT_MAIN_BRANCH}
fi

popd

echo "DONE"
