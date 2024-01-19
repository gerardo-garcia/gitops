#!/usr/bin/python3

# ./gitops.py

import yaml
import json
import argparse
import logging
import randomname
import random
import string
from libs import common, operations as ops


####################################
# Global functions
####################################
def print_yaml_json(document, to_json=False):
    if to_json:
        print(json.dumps(document, indent=4))
    else:
        print(yaml.safe_dump(document, indent=4, default_flow_style=False, sort_keys=False))


def set_logger(verbose):
    global logger
    log_format_simple = "%(levelname)s %(message)s"
    log_format_complete = "%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)s %(funcName)s(): %(message)s"
    log_formatter_simple = logging.Formatter(log_format_simple, datefmt="%Y-%m-%dT%H:%M:%S")
    handler = logging.StreamHandler()
    handler.setFormatter(log_formatter_simple)
    logger = logging.getLogger("gitops")
    logger.setLevel(level=logging.WARNING)
    logger.addHandler(handler)
    if verbose == 1:
        logger.setLevel(level=logging.INFO)
    elif verbose > 1:
        log_formatter = logging.Formatter(log_format_complete, datefmt="%Y-%m-%dT%H:%M:%S")
        handler.setFormatter(log_formatter)
        logger.setLevel(level=logging.DEBUG)


def generate_random_name():
    random_name = randomname.get_name() + "-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=7))
    return random_name


####################################
# Operations
####################################
def testOperationSequence():
    # Creates a sequence of operations
    operations = []
    cluster_name = generate_random_name()
    operation1 = ops.createClusterOperation(
        which=cluster_name,
        params={
            "name": cluster_name,
            "node_count": "1",
            "k8s_version": "1.25",
            "node_size": "Standard_D2_v2",
            "cluster_location": "West Europe",
            "resource_group": "CloudNative-InfraMgmt-CTIO",
        },
    )
    operations.append(operation1)
    operation2 = ops.scaleClusterOperation(which=cluster_name, params={"node_count": "2"})
    operations.append(operation2)
    operation3 = ops.deleteClusterOperation(
        which=cluster_name,
    )
    operations.append(operation3)
    return operations


####################################
# Main
####################################
if __name__ == "__main__":
    # Argument parse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--repo",
        default="git@github.com:gerardo-garcia/gitops.git",
        help="git repository to be used",
    )
    # parser.add_argument(
    #     "-c",
    #     "--catalog",
    #     default="sw-catalogs",
    #     help="folder in git repository that stores the templates",
    # )
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity")
    args = parser.parse_args()

    # Initialize logger
    set_logger(args.verbose)

    # Define operations
    operations = testOperationSequence()
    logger.info(f"Testing {len(operations)} operations:")
    for op in operations:
        op_info = f"Operation {op['id']}: {op['op']} {op['what']} {op['which']}"
        logger.info(f"- {op_info}")
    input("Press Enter to proceed...")

    logger.debug(f"Operations:\n{yaml.safe_dump(operations, indent=4, default_flow_style=False, sort_keys=False)}")

    # Execution of operations
    for op in operations:
        try:
            op_info = f"Operation {op['id']}: {op['op']} {op['what']} {op['which']}"
            logger.info(f"{op_info}, params: {op.get('patch','None')}")
            logger.info("Step 1. Clone Git Repo and create branch")
            input("Press Enter to proceed...")
            repo_dir = common.cloneGitRepo(repo_url=args.repo, branch=f"op-{op['id']}")
            logger.info("Step 2. Create/Update/Delete Kubernetes Manifests")
            input("Press Enter to proceed...")
            common.prepareManifests(repo_dir, op)
            logger.info("Step 3. Create Commit in local Branch")
            input("Press Enter to proceed...")
            git_branch = common.createCommit(repo_dir, commit_msg=op_info)
            logger.info("Step 4. Merge local branch in main")
            input("Press Enter to proceed...")
            result = common.mergeGit(repo_dir, git_branch)
            logger.info(f"Merge result: {result}")
            if not result:
                raise Exception("Failed merge")
            logger.info("Step 5. Push changes to remote")
            input("Press Enter to proceed...")
            result = common.pushToRemote(repo_dir)
            input("Press Enter to continue...")
        except Exception:
            raise Exception()
