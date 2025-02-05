#! /usr/bin/env python3

import os
import git
import subprocess

def run_command(command, cwd=None):
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}\n{result.stderr}")
    return result.stdout

REPO_URL = "https://github.com/bluerobotics/BlueOS-docs"
CLONE_DIR = "repository"

# Clone the repository or open existing one
if not os.path.exists(CLONE_DIR):
    repo = git.Repo.clone_from(REPO_URL, CLONE_DIR)
else:
    repo = git.Repo(CLONE_DIR)
    print("Repository already cloned.")

if os.path.exists('docs'):
    print("Removing existing docs folder...")
    run_command("rm -rf docs/*")

# Fetch all branches
repo.remotes.origin.fetch()
branches = [ref.name.split('/')[-1] for ref in repo.remotes.origin.refs if not ref.name.endswith('HEAD')]

# Run zola build on each branch
for branch in branches:
    print(f"\nSwitching to branch: {branch}")
    repo.git.checkout(branch)
    print("Initializing and updating submodules...")
    repo.git.submodule('init')
    repo.git.submodule('update')
    run_command(f"zola build --base-url /docs/{branch}", cwd=CLONE_DIR)
    print(f"Build completed for branch: {branch}\n")

    # Create branch directory in docs and move public folder content there
    branch_dir = os.path.join('docs', branch)
    if not os.path.exists(branch_dir):
        os.makedirs(branch_dir)
    run_command(f"mv {CLONE_DIR}/public/* {branch_dir}/")

# Copy data.json to docs directory if it exists in the repository
if os.path.exists("data.json"):
    run_command(f"cp data.json docs/")
