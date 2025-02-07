#! /usr/bin/env python3

import os
import git
import subprocess

def run_command(command, cwd=None):
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}\n{result.stderr}")
    return result.stdout

ORG_URL = "https://github.com/bluerobotics"
REPOS = {
    "BlueOS-docs": ["latest", "stable"],
    "Cockpit-docs": ["latest"],
}

if os.path.exists('docs'):
    print("Removing existing docs folder...")
    run_command("rm -rf docs/*")

for repo_name, branches in REPOS.items():
    if not os.path.exists(repo_name):
        repo = git.Repo.clone_from(f"{ORG_URL}/{repo_name}", repo_name)
    else:
        repo = git.Repo(repo_name)
        print("Repository already cloned.")

    # Run zola build on each branch
    for branch in branches:
        site_name = f"{repo_name.replace('-docs', '')}-{branch}"
        print(f"\nSwitching to: {site_name}")
        repo.git.checkout(branch)
        print("Initializing and updating submodules...")
        repo.git.submodule('init')
        repo.git.submodule('update')
        build_command = "zola "
        if os.path.exists(os.path.join(repo_name, "config.extension.toml")):
            build_command += "--config config.extension.toml build"
        else:
            build_command += f"build --base-url /docs/{site_name}"
        run_command(build_command, cwd=repo_name)
        print(f"Build completed for: {site_name}\n")

        # Create branch directory in docs and move public folder content there
        branch_dir = os.path.join('docs', site_name)
        if not os.path.exists(branch_dir):
            os.makedirs(branch_dir)
        run_command(f"mv {repo_name}/public/* {branch_dir}/")

# Copy data.json to docs directory if it exists in the repository
if os.path.exists("data.json"):
    run_command(f"cp data.json docs/")
