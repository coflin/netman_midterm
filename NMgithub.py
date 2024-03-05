import os
from git import Repo

def get_or_create_repo():
    # Get the current working directory
    cwd = os.getcwd()

    try:
        # Initialize the repository object
        repo = Repo(cwd)
        print(repo)
        return repo
    except:
        # If initialization fails, create a new repository
        repo = Repo.init(cwd)
        return repo

def push_latest_modified_files(file_extensions):
    repo = get_or_create_repo()

    # Fetch the latest changes from the remote repository
    origin = repo.remote(name='origin')
    origin.fetch()

    # Get the current branch name
    branch_name = repo.active_branch.name

    # Compare local and remote branches to find modified files
    for item in repo.index.diff(None):
        print(item.a_path)


    # changed_files = [item.a_path for item in repo.index.diff(None) if item.a_path.endswith(file_extensions)]

    # # Stage all modified files
    # print(F"Staging these modified files: {changed_files}")
    # repo.index.add(changed_files)

    # print("Committing the changes..")
    # # Commit the changes
    # repo.index.commit("Committing modified files in the working directory")

    # print("Pushing to the remote repository")
    # # Push the changes to the remote repository
    # origin.push(branch_name)
    # print("Pushed to the repository.")

push_latest_modified_files(('.txt','.jpg'))