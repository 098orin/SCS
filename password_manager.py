import sys
import value
import fun
import crpt
import time
from rich.console import Console
import scratchattach as scratch3
import re

try:
    arg = str(sys.argv[1])
except IndexError:
    arg = ""

chars = "-^~=)('&%$#!abcdefghijklmnopqrstuvwxyz@[;:],./<>?_+*}`ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛｦﾝ"
test_chars = "1234567890-^~=)('&%$#!abcdefghijklmnopqrstuvwxyz@[;:],./<>?_+*}`ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛｦﾝｧｨｩｪｫｬｭｮｯ"
print(len(chars))

datadir = value.datadir
project_id = value.password_project
console = Console()

project = scratch3.get_project(project_id)

from cryptography.hazmat.primitives.asymmetric import x448
from cryptography.hazmat.primitives import serialization

def generate_key_pair():
    """Curve448の秘密鍵と公開鍵を生成する"""
    private_key = x448.X448PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key

def exchange_keys(private_key, peer_public_key):
    """共有鍵を計算する"""
    if isinstance(private_key, int):
        private_key = format(private_key, "x")
    if isinstance(peer_public_key, int):
        peer_public_key = format(peer_public_key, "x")
    if isinstance(private_key, str):
        private_key = x448.X448PrivateKey.from_private_bytes(bytes.fromhex(private_key))
    if isinstance(peer_public_key, str):
        peer_public_key = x448.X448PublicKey.from_public_bytes(bytes.fromhex(peer_public_key))
    shared_key = private_key.exchange(peer_public_key)
    return shared_key

def key_to_hex(key):
    """鍵を16進数に変換する"""
    try:
        bytes = key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
    except AttributeError:
        bytes = key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
    return bytes.hex()

def to_string_(number):
    """
    数値を文字列に変換する
    """
    global chars
    result = ""
    for i in range(int(len(number)/2)):
        i = 2*i
        result += str(chars[int(number[i:i+2])])
    if len(number) % 2 == 1:
        result += str(number[i])
    return result

def is_official(text):
  """
  文字列が英数字、ハイフン、アンダースコア、コロンのみで構成されているかチェックする
  """
  return bool(re.match("^[a-zA-Z0-9\\-_,]+$" + chars, text))

def purse_comment(comment):
    """
    purse the comment
    """
    comment_data = comment.content
    comment_author = comment.author_name
    if is_official(comment_data) and comment_author == comment_data[len(comment_author)]:
        data = comment_data.split(",")
        if len(data) != 3:
            console.log("Invalid comment format")
            return False
        return True
    else:
        return False


def set_password(comment):
    """
    Set the password for the user by the project comment.
    """
    user = comment.author_name
    data = comment.content.split(",")
    user_public_key = data[1]
    encrypted_password = data[2]

    console.log("set password")
    path = datadir + "/password/" + user + "password.txt"
    if fun.file_exists(path):
        console.log("password file already exists")
        console.log("change password")
    pass
    
if arg == "gen":
    public_key, private_key = generate_key_pair()
    private_key, public_key = key_to_hex(private_key), key_to_hex(public_key)
    print(f"公開鍵：{public_key}")
    print(f"秘密鍵：{private_key}")
    print("README.md を参照して、適切に処理してください。")
else:
    while True:
        comments = project.comments(limit=10)
        for comment in comments:
            if purse_comment(comment):
                set_password(comment)
        time.sleep(60)  # 60秒待機
