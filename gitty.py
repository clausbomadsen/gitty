#!/usr/bin/python3

# todo:
    # rebase-onto
    # checkout-local
    # diff
    # clean-up branched
    # search feature branch
    
from tabnanny import check
import click
from subprocess import check_output, check_call

def get_current_branch():
    return check_output(["git", "branch", "--show-current"], text=True).rstrip("\n")

def git_checkout(branch):
    check_call(["git", "checkout", branch])

def git_pull():
    check_call(["git", "pull"])   

def git_rebase(branch):
    check_call(["git", "rebase", branch])

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
    git_rebase(branch)
        
    print(f"git rebase {get_current_branch()} {branch}")

if __name__ == "__main__":
    gitty()