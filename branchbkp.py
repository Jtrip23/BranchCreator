import os
import pandas as pd
from github import Github
import logging

logging.basicConfig(level=logging.INFO)

def rename_branch(username, token, repo_name, old_branch_name, new_branch_name):
    try:
        g = Github(username, token)
        repo = g.get_repo(f"{username}/{repo_name}")
        
        # Check if the old branch exists
        try:
            old_branch = repo.get_branch(old_branch_name)
            logging.info(f"Branch '{old_branch_name}' found in '{repo_name}', proceeding with renaming.")
            
            # Create the new branch as a backup
            new_ref = repo.create_git_ref(
                ref=f"refs/heads/{new_branch_name}",
                sha=old_branch.commit.sha
            )
            logging.info(f"Branch '{old_branch_name}' renamed to '{new_branch_name}' in '{repo_name}'.")

            # Optional: Delete the old branch (if desired)
            # repo.get_git_ref(f"refs/heads/{old_branch_name}").delete()
            # logging.info(f"Old branch '{old_branch_name}' deleted from '{repo_name}'.")

        except Exception as e:
            logging.error(f"Branch '{old_branch_name}' not found in '{repo_name}': {e}")
            
    except Exception as e:
        logging.error(f"Error renaming branch in '{repo_name}': {e}")

def rename_branches_from_excel(username, token, excel_file):
    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
        
        # Define old and new branch mappings
        branch_mappings = {
            'development': 'developmentbkp',
            'integration': 'integrationbkp',
            'release': 'releasebkp'
            'feature': 'featurebkp'
        }

        for index, row in df.iterrows():
            repo_name = row['repo_name']
            
            for old_branch, new_branch in branch_mappings.items():
                rename_branch(username, token, repo_name, old_branch, new_branch)

    except Exception as e:
        logging.error(f"Error reading Excel file or renaming branches: {e}")

if __name__ == "__main__":
    username = os.getenv('USERNAME')
    token = os.getenv('TOKEN')
    excel_file = 'repositories.xlsx'  # Path to your Excel file

    if not (username and token):
        logging.error("GitHub credentials not provided. Set USERNAME and TOKEN environment variables.")
    else:
        rename_branches_from_excel(username, token, excel_file)
