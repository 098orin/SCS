version v.1.2.0
# SCS (Sratch Cloud System)
これはscratch projectと外部での通信を可能にするためのサーバープログラムです。

# Setup
git cloneします。
```bash
git clone https://github.com/098orin/SCS.git
```

プロジェクトのルート下に`value.py`というファイルを作成します。
```py
username = your_username   # string
password = your_password   # string
path = "your_path" # string このrepositoryの絶対path
datadir = "data_directory_path" # string "/SCS_data"の絶対パス
project_id = [your_project_ids]   # 型は指定しない。数字で普通にプロジェクトidを書いてください。
project_client = [your_project_client]   # Scratchの場合は"sc", Turbowarpの場合は"tw"
project_privilege = [project_privileges]   # 信頼できるprojectは"high", 普通のは"low"
```
`project_なんたら`はそれぞれの一番目はすべて同じプロジェクトのことになるように全部リストの番号と内容を合わせてください。

最初に`setup.py`を動かす必要があった気がしないでもないです。もし動かなかったらこれを実行してみてください。

# Run
実行にはpythonが必要です。それ以外は必要ありません。管理者権限があるとなお良いです。
すべてのOSで動くように作っていますが、動作確認はWindwsとLinuxのみです。

Windws, macOS, Linux
```bash
cd SCS
python _server.py
```

Linuxはできれば
```bash
cd SCS
sudo python _server.py
```
のほうが好ましいです。権限Ｅｒｒｏｒで動かないかもしれません。もし動かなかったら教えてください。