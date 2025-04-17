# デバッグ実行について

## .envファイルの追加とTOKENの設定

.envファイルをsrcファイル直下に配置する
.envファイルに以下の記述を追加し、保存する

```text
#!/.env
TOKEN={discord bot token}
```

## ローカルの.envファイルをdocker内の.envファイルと同期させる

```bash
#!/.env
docker cp ./.env withQ_project:/root/.env
```

## docker build

```bash
#!/~
docker compose up -d --build
#or
docoker build ./ -t withq
```

## コンテナのターミナルへ接続する

```bash
#!/~
docker compose exec python3 bash
#or
docker run --name withq -it withq
```

## コードの実行

※dockerのコンテナ内のbashで実行

```bash
#!~/withQ
python main.py
```

## 本番環境用リポジトリとの同期

```bash
#!~ withQ/master
git fetch upstream
git merge --allow-unrelated-histories upstream/master
```
