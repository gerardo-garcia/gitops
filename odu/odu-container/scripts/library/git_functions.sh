#!/bin/bash

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

write_sshkey() {
    echo "Writing GIT_SSHKEY in $HOME/.ssh/id_rsa"
    mkdir $HOME/.ssh
    echo "${GIT_SSHKEY}" | base64 -d > $HOME/.ssh/id_rsa
    chmod 700 $HOME/.ssh/id_rsa
    echo "... DONE"
}

config_local_git_user_email() {
    echo "Setting git local user and e-mail in current folder"
    git config --local user.email "${GIT_USER_EMAIL}"
    git config --local user.name "${GIT_USER_NAME}"
    echo "... DONE"
}
