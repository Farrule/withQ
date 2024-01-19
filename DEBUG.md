# .envファイルの追加とTOKENの設定

.envファイルをsrcファイル直下に配置する
.envファイルに以下の記述を追加し、保存する

```
TOKEN={discord bot token}
```

# docker build

```
docker compose up -d --build
```

# コンテナのターミナルへ接続する

```
docker compose exec python3 bash
```

# コードの実行

```
cd src
python test.py
```