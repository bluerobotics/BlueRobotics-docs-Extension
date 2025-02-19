#! /usr/bin/env python3

import subprocess
from pathlib import Path

def run_command(command, cwd=None):
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}\n{result.stderr}")
    return result.stdout

if Path('docs').exists():
    print("Removing existing docs folder...")
    run_command("rm -rf docs/*")

for repo in Path('src').iterdir():
    build_command = 'zola '
    if (repo / "config.extension.toml").exists():
        build_command += '--config config.extension.toml build'
    else:
        build_command += f'build --base-url /docs/{repo.name}'
    run_command(build_command, cwd=repo)
    print(f"Build completed for: {repo.name}\n")

    # Create branch directory in docs and move public folder content there
    branch_dir = Path('docs') / repo.name
    branch_dir.mkdir(parents=True, exist_ok=True)
    run_command(f"mv {repo}/public/* {branch_dir}/")

# Copy data.json to docs directory if it exists in the repository
if Path('data.json').exists():
    run_command("cp data.json docs/")
