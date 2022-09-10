#!/usr/bin/python3

# todo:
    # checkout-local
    # diff
    # clean-up branched
    # search feature branch
    
import click
from subprocess import STDOUT, CalledProcessError, check_output, check_call

def get_current_branch():
    return check_output(["git", "branch", "--show-current"], text=True).rstrip("\n")

def git_checkout(branch):
    check_call(["git", "checkout", branch])

def git_pull() -> bool:
    try:
        check_output(["git", "pull"], text=True, stderr=STDOUT)   
    except CalledProcessError as e:
        output = str(e.output)
        if output.startswith("There is no tracking information for the current branch."):
            print("No tracking information for the current branch.")
            return False
        else:
            raise e
    else:
        return True

def git_rebase(branch) -> bool:
    try:
        check_output(["git", "rebase", branch], text=True, stderr=STDOUT)
    except CalledProcessError as e:
        output = str(e.output)
        if "CONFLICT" in output:
            for line in output.splitlines():
                if "conflict in" in line:
                    print(line)
            return False
        else:
            raise e
    else:
        return True
    
def git_status() -> str:
    return check_output(["git", "status"], text=True, stderr=STDOUT)


def open_in_vscode(filename):
    check_call(["code", filename])
    

@click.group("gitty")
def gitty():
    pass

@gitty.command("rebase", help="Pull target branch and rebase current branch upon it.")
@click.argument("branch")
@click.option("--no-pull", is_flag=True, help="Don't pull the target branch")
@click.option("--allow-master", is_flag=True, help="Allow rebasing upon master.")
def rebase(branch, allow_master, no_pull):
    source_branch = get_current_branch()
    if not no_pull:
        git_checkout(branch)
        git_pull()
    git_checkout(source_branch)
    if not git_rebase(branch):
        for line in git_status().splitlines():
            if "modified" in line:
                open_in_vscode(line.split()[-1])
                
        
if __name__ == "__main__":
    gitty()