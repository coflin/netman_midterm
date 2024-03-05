import os
from git import Repo

def get_or_create_repo():
    # Get the current working directory
    cwd = os.getcwd()

    try:
        # Try to initialize the repository object
        repo = Repo(cwd)
        print(repo)
        return repo
    except:
        # If initialization fails, create a new repository
        repo = Repo.init(cwd)
        return repo

def push_all_files():
    repo = get_or_create_repo()

    # Stage all files
    repo.index.add("*")

    # Commit the changes
    repo.index.commit("Committing all files in the working directory")

    # Push the changes to the remote repository
    origin = repo.remote(name='origin')
    origin.push()

push_all_files()
