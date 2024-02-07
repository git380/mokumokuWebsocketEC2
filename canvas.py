import asyncio
import json

import websockets

# クライアントの管理用のセット
clients = set()


async def echo(websocket):
    # 接続が確立された
    print('canvas-クライアントが接続しました。')
    # 新しいクライアントのWebSocket接続をclientsセットに追加
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            uuid = data[0]
            # JSONのチャット履歴を追加
            with open('json/canvas_history.json', 'r', encoding='utf-8') as json_file_r:
                canvas_history = json.load(json_file_r)
            # クリアイベントの処理
            if data[1] == 'clear':
                canvas_history[uuid].clear()
            else:
                data = data[1:]
                # 短縮形16進数の色コードに変換
                color = '#{:02x}{:02x}{:02x}'.format(*map(int, data[0][4:-1].split(', ')))
                data[0] = color[:2] + color[3] + color[5]
                # JSONチャット履歴を辞書に追加(キーはStringに変換)
                if uuid in canvas_history:
                    canvas_history[uuid].append(data)
                else:
                    canvas_history[uuid] = [data]
            # チャット履歴をJSONで保存
            with open('json/canvas_history.json', 'w', encoding='utf-8') as json_file_w:
                json.dump(canvas_history, json_file_w, ensure_ascii=False, indent=4)
            # クライアントからのお絵かきデータをすべてのクライアントにブロードキャスト
            for client in clients:
                if client != websocket:
                    # 自分以外の全員に送る
                    await client.send(message)
    finally:
        # クライアントが切断された場合、セットから削除
        clients.remove(websocket)
        print('canvas-接続が切断されました。')

start_server = websockets.serve(echo, '0.0.0.0', 8124)
print('canvas-サーバー起動中...')

# イベントループの開始
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
