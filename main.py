import subprocess

# notionサーバを実行
notion = subprocess.Popen(['python', 'notion.py'], start_new_session=True)

# チャットサーバを実行
chat = subprocess.Popen(['python', 'chat.py'], start_new_session=True)

# キャンバスサーバを実行
canvas = subprocess.Popen(['python', 'canvas.py'], start_new_session=True)

pseudo_lambda = subprocess.Popen(['python', 'api_server.py'], start_new_session=True)

notion.wait()
chat.wait()
canvas.wait()
