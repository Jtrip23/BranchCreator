import os
import pandas as pd
from github import Github
import logging

logging.basicConfig(level=logging.INFO)

def create_branch(username, token, repo_name, base_branch, new_branch_names):
    try:
        g = Github(username, token)
        repo = g.get_repo(f"{username}/{repo_name}")
        base_ref = repo.get_branch(base_branch)
        for branch in new_branch_names:
            try:
                # Check if the branch already exists
                repo.get_branch(branch)
                logging.info(f"Branch '{branch}' already exists in '{repo_name}'. Skipping creation.")
            except Exception as e:
                # If branch doesn't exist, create it
                new_ref = repo.create_git_ref(
                    ref=f"refs/heads/{branch}",
                    sha=base_ref.commit.sha
                )
                logging.info(f"Branch '{branch}' created successfully in '{repo_name}'.")
    except Exception as e:
        logging.error(f"Error creating branches in '{repo_name}': {e}")

def create_branches_from_excel(username, token, excel_file):
    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
        for index, row in df.iterrows():
            repo_name = row['source_repo_name']
            base_branch = 'release'
            new_branch_names = ['feature_cloudhub', 'development_cloudhub', 'integration_cloudhub', 'release_cloudhub']
            create_branch(username, token, repo_name, base_branch, new_branch_names)
    except Exception as e:
        logging.error(f"Error reading Excel file or creating branches: {e}")

if __name__ == "__main__":
    username = os.getenv('USERNAME')
    token = os.getenv('TOKEN')
    excel_file = 'repositories.xlsx'  # Path to your Excel file

    if not (username and token):
        logging.error("GitHub credentials not provided. Set USERNAME and TOKEN environment variables.")
    else:
        create_branches_from_excel(username, token, excel_file)
