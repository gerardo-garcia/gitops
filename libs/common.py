import tempfile
import logging
from git import Repo
import jsonpatch
import yaml
import os
import shutil

logger = logging.getLogger("gitops")


def cloneGitRepo(repo_url):
    tmpdir = tempfile.mkdtemp()
    logger.debug(f"Created temp folder {tmpdir}")
    repo = Repo.clone_from(repo_url, tmpdir)
    assert repo
    logger.info(f"Repo {repo_url} cloned in {tmpdir}")
    return tmpdir


def pushToGit(repo_dir):
    print(repo_dir)
    # add
    # commit
    #
    # if recursive:
    #     descriptors_paths = [
    #         f for f in glob.glob(base_directory + "/**/*.yaml", recursive=recursive)
    #     ]
    # else:
    #     descriptors_paths = [
    #         f for f in glob.glob(base_directory + "/*.yaml", recursive=recursive)
    #     ]
    # update_file = "dir1/file2.txt"  # we'll use local_dir/dir1/file2.txt
    # with open(f"{local_dir}/{update_file}", "a") as f:
    # f.write("\nUpdate version 2")
    return "branch"


def mergeGit(repo_dir, git_branch):
    return True


def prepareManifests(repo_dir, operation):
    MANIFEST_BASE_FOLDER = "managed-resources"
    OPERATIONS_MAP = {
        "cluster": {
            "dir": "clusters",
            "template_folder": "sw-catalogs/cluster-aks",
            "template": "cluster.yaml",
        }
    }
    operation_dir = OPERATIONS_MAP[operation["what"]]["dir"]
    manifests_dir = f"{MANIFEST_BASE_FOLDER}/{operation_dir}/{operation['which']}"

    if operation["op"] == "delete":
        # If operation is delete, delete the folder "manifest_dir"
        shutil.rmtree(path=manifests_dir)
    else:
        if operation["op"] == "create":
            # If operation is create, create the folder "manifest_dir"
            try:
                os.makedirs(manifests_dir)
                logger.info(f"Folder {manifests_dir} created!")
            except FileExistsError:
                logger.error("Folder {manifests_dir} already exists")
            # and copy content from template_folder
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
                f"Original manifest: {yaml.safe_dump(original_dict, indent=2, default_flow_style=False, sort_keys=False)}"
            )
        # Update dictionary with patch from operation
        patch = jsonpatch.JsonPatch(operation["patch"])
        logger.debug(f"Patch: {yaml.safe_dump(patch, indent=2, default_flow_style=False, sort_keys=False)}")
        result_dict = patch.apply(original_dict)
        logger.debug(f"Resulting manifest: {yaml.safe_dump(result_dict, indent=2, default_flow_style=False, sort_keys=False)}")
        with open(manifest_file, "w") as output:
            yaml.safe_dump(result_dict, output, indent=2, default_flow_style=False, sort_keys=False)
            logger.info(f"Manifest written to file {manifest_file} successfully")
