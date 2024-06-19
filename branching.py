import os
from github import Github
import pandas as pd

def create_branch(username, token, repo_name, base_branch, new_branch_name):
    try:
        g = Github(username, token)
        repo = g.get_repo(f"{username}/{repo_name}")
        base_ref = repo.get_branch(base_branch)
        new_ref = repo.create_git_ref(
            ref=f"refs/heads/{new_branch_name}",
            sha=base_ref.commit.sha
        )
        print(f"Branch '{new_branch_name}' created successfully in '{repo_name}'.")
    except Exception as e:
        print(f"Error creating branch in '{repo_name}': {e}")

def create_branches_from_excel(username, token, excel_file):
    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
        for index, row in df.iterrows():
            repo_name = row['name']
            base_branch = row['base_branch']
            new_branch_name = row['new_branch']
            create_branch(username, token, repo_name, base_branch, new_branch_name)
    except Exception as e:
        print(f"Error reading Excel file or creating branches: {e}")

if __name__ == "__main__":
    username = os.getenv('USERNAME')
    token = os.getenv('TOKEN')
    excel_file = 'repositories.xlsx'  # Path to your Excel file
    create_branches_from_excel(username, token, excel_file)
