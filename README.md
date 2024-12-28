# SCS (Sratch Cloud System)
これはscratch projectと外部での通信を可能にするためのサーバープログラムです。

# Setup
value.py というファイルを作成します。
```py
username = your_username   // string
password = your_password   // string
project_id = [your_project_ids]   //型は指定しない。数字で普通にプロジェクトidを書いてください。
project_client = [your_project_client]   // Scratchの場合は"sc", Turbowarpの場合は"tw"
project_privilege = [project_privileges]   // 信頼できるprojectは"high", 普通のは"low"
```
`project_なんたら`はそれぞれの一番目はすべて同じプロジェクトのことになるように全部リストの番号と内容を合わせてください。
