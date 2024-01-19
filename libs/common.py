import tempfile
import logging
from git import Repo
import jsonpatch
import yaml
import os
import shutil

logger = logging.getLogger("gitops")


def cloneGitRepo(repo_url, branch):
    tmpdir = tempfile.mkdtemp()
    logger.debug(f"Created temp folder {tmpdir}")
    cloned_repo = Repo.clone_from(repo_url, tmpdir)
    logger.debug(f"Current active branch: {cloned_repo.active_branch}")
    assert cloned_repo
    new_branch = cloned_repo.create_head(branch)  # create a new branch
    assert (new_branch.checkout() == cloned_repo.active_branch)
    logger.debug(f"Current active branch: {cloned_repo.active_branch}")
    logger.info(f"Repo {repo_url} cloned in {tmpdir}. New branch: {branch}")
    return tmpdir


def createCommit(repo_dir, commit_msg):
    repo = Repo(repo_dir)
    logger.info(f"Creating commit '{commit_msg}' in branch '{repo.active_branch}'")
    logger.debug(f"Current active branch: {repo.active_branch}")
    # repo.index.add('**')
    repo.git.add(all=True)  # With repo.git you can do anything you can do with git cmd
    repo.index.commit(commit_msg)
    logger.info(f"Commit '{commit_msg}' created in branch '{repo.active_branch}'")
    logger.debug(f"Current active branch: {repo.active_branch}")
    return repo.active_branch


def mergeGit(repo_dir, git_branch):
    repo = Repo(repo_dir)
    logger.info(f"Merging local branch '{git_branch}' into main")
    with_git = False
    if with_git:
        try:
            repo.git("checkout main")
            repo.git(f"merge {git_branch}")
            return True
        except Exception as e:
            logger.error(e)
            return False
    else:
        # prepare a merge
        main = repo.heads.main  # right-hand side is ahead of us, in the future
        merge_base = repo.merge_base(git_branch, main)  # allows for a three-way merge
        repo.index.merge_tree(main, base=merge_base)  # write the merge result into index
        try:
            # The merge is done in the branch
            repo.index.commit(
                f"Merged {git_branch} and main into {git_branch};)",
                parent_commits=(git_branch.commit, main.commit),
            )
            # Now, git_branch is ahed of master. Now let master point to the recent commit
            aux_head = repo.create_head("aux")
            main.commit = aux_head.commit
            repo.delete_head(aux_head)
            assert main.checkout()
            return True
        except Exception as e:
            logger.error(e)
            return False


def pushToRemote(repo_dir):
    repo = Repo(repo_dir)
    logger.info(f"Pushing the change to remote")
    # repo.remotes.origin.push(refspec='{}:{}'.format(local_branch, remote_branch))
    repo.remotes.origin.push()
    logger.info(f"DONE")


def prepareManifests(repo_dir, operation):
    OPERATIONS_MAP = {
        "cluster": {
            "dir": "clusters",
            "template_dir": "sw-catalogs/cluster-aks",
            "template": "cluster.yaml",
        }
    }
    manifest_base_folder = f"{repo_dir}/managed-resources"
    operation_dir = OPERATIONS_MAP[operation["what"]]["dir"]
    manifests_dir = f"{manifest_base_folder}/{operation_dir}/{operation['which']}"
    if operation["op"] == "delete":
        # If operation is delete, delete the folder "manifest_dir"
        logger.info(f"Manifests in {manifests_dir} will be deleted")
        shutil.rmtree(path=manifests_dir)
        logger.info(f"Deleted")
    else:
        if operation["op"] == "create":
            # If operation is create, create the folder "manifest_dir"
            logger.info(f"Manifests will be created in {manifests_dir}")
            # Este código se puede evitar y hacer que la copia con shutil.copytree cree el directorio
            try:
                os.makedirs(manifests_dir)
                logger.info(f"Folder {manifests_dir} created!")
            except FileExistsError:
                logger.error(f"Folder {manifests_dir} already exists")
            # And copy content from template_dir
            template_dir = OPERATIONS_MAP[operation["what"]]["template_dir"]
            origin = f"{repo_dir}/{template_dir}"
            logger.debug(f"Before: {os.listdir(manifests_dir)}")
            logger.debug(f"Copying from {origin} to {manifests_dir}")
            shutil.copytree(origin, manifests_dir, dirs_exist_ok=True)
            logger.debug(f"After: {os.listdir(manifests_dir)}")
        elif operation["op"] == "update":
            # If operation is update, the folder "manifest_dir" should exist
            if os.path.isdir(manifests_dir):
                logger.info("Folder %s exists" % manifests_dir)
            else:
                logger.error("Folder %s does no exist exists" % manifests_dir)
        # For both operations (update, create), files are edited
        # Open manifests_dir/template file and load it as dict
        manifest_file = f"{manifests_dir}/{OPERATIONS_MAP[operation['what']]['template']}"
        with open(manifest_file, "r") as mf:
            original_dict = yaml.safe_load(mf.read())
            logger.debug(
                f"Original manifest:\n{yaml.safe_dump(original_dict, indent=2, default_flow_style=False, sort_keys=False)}"
            )
        # Update dictionary with patch from operation
        patch = jsonpatch.JsonPatch(operation["patch"])
        # logger.debug(f"Patch:\n{json.dumps(operation['patch'], indent=2)}")
        logger.debug(f"Patch:\n{patch}")
        result_dict = patch.apply(original_dict)
        logger.debug(f"Resulting manifest:\n{yaml.safe_dump(result_dict, indent=2, default_flow_style=False, sort_keys=False)}")
        with open(manifest_file, "w") as output:
            yaml.safe_dump(result_dict, output, indent=2, default_flow_style=False, sort_keys=False)
            logger.info(f"Manifest written to file {manifest_file} successfully")
