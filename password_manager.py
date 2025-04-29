import value
import fun
import time
from rich.console import Console
import scratchattach as scratch3
import re

datadir = value.datadir
project_id = value.password_project
console = Console()

project = scratch3.get_project(project_id)

def is_alphanumeric_with_hyphen_underscore(text):
  """
  文字列が英数字、ハイフン、アンダースコアのみで構成されているかチェックする
  """
  return bool(re.match("^[a-zA-Z0-9\\-_]+$", text))

def purse_comment(comment):
    """
    purse the comment
    """
    comment_data = comment.content
    comment_author = comment.author_name
    if is_alphanumeric_with_hyphen_underscore(comment_data) and comment_author == comment_data[len(comment_author)]:
        return True
    else:
        return False


def set_password(comment):
    """
    Set the password for the user by the project comment.
    """
    user = comment.author_name
    encrypted_password = comment.content[len(user):]

    console.log("set password")
    path = datadir + "/password/" + user + "password.txt"
    if fun.file_exists(path):
        console.log("password file already exists")
        console.log("change password")
    

while True:
    project.comments(limit=3)
    for comment in project.comments(limit=3):
        if purse_comment(comment):
            set_password(comment)
    time.sleep(60)  # 60秒待機