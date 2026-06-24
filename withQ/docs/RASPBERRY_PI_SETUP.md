# Raspberry Pi 常駐化環境 構築手順書・仕様書

本ドキュメントは、Windows PC上で稼働していた `withQ` を **Raspberry Pi** へ移行し、常時稼働（常駐化）させるための環境構築手順と移行後の運用仕様をまとめたものです。

---

## 1. 移行後の動作・インフラ仕様

- **対象ハードウェア**: Raspberry Pi 3 / 4 / 5（Raspberry Pi OS 32bit / 64bit）
- **コンテナベース**: `python:3.10-slim` (ARM / x86_64 両対応の軽量公式マルチプラットフォームイメージ)
- **常駐化ポリシー**: `restart: unless-stopped`
  - Raspberry Pi自体の再起動、またはDockerデーモンの起動時に自動的にBotコンテナが復帰・常駐起動します。
- **ボイス機能関連パッケージの非搭載化**:
  - 本Botではボイス機能（VC接続・再生）を使用しないため、ビルド時間とイメージサイズ削減を目的として `PyNaCl` および `ffmpeg` パッケージを除外した軽量構成に最適化されています。

---

## 2. 構築手順

Raspberry Pi上でターミナルを起動し、以下の手順に沿って環境構築を勧めます。

### ステップ 1: OSのアップデート

最初にシステムパッケージを最新の状態にします。

```bash
sudo apt update && sudo apt upgrade -y
```

### ステップ 2: Docker および Docker Compose のインストール

Raspberry Pi OSに公式の自動インストールスクリプトを用いてDockerをインストールします。

```bash
# Dockerのインストール
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 現在のユーザーをdockerグループに追加 (これにより sudo なしで docker コマンドが実行可能になります)
sudo usermod -aG docker $USER
```

※グループ追加を反映させるため、一度ログアウトして再ログインするか、`newgrp docker` コマンドを実行してください。

### ステップ 3: プロジェクトソースコードの取得

Gitを使用して、リポジトリをRaspberry Pi上の任意の場所にクローンします。

```bash
cd ~
git clone https://github.com/Farrule/withQ.git
cd withQ
```

### ステップ 4: 環境変数 (.env) の設定

`.env` ファイルを作成し、Discord Botのトークンや起動環境（本番 or デバッグ）を指定します。

```bash
# .envファイルを新規作成して編集
nano .env
```

**`.env` ファイルの記述内容**:

```text
EXECUTION_ENV=PRODUCTION
PRODUCTION_TOKEN=あなたの本番用DiscordBotトークン
DEVELOPMENT_TOKEN=あなたの開発デバッグ用DiscordBotトークン
```

_（※ `Ctrl + O` -> `Enter` で保存、`Ctrl + X` で終了します）_

### ステップ 5: コンテナのビルドとバックグラウンド起動

Docker Compose を使用してコンテナを構築し、バックグラウンド（デタッチモード）で起動します。

```bash
docker compose up -d --build
```

### ステップ 6: 動作・ログ監視の確認

起動が成功しているかログを確認します。

```bash
docker compose logs -f
```

正常にBotが起動していれば、ログに `Logged in as withQ...` や `Update success!` と出力されます。

---

## 3. 常駐・メンテナンス・運用の仕様

### 3.1 自動再起動の挙動

`docker-compose.yml` で設定されている `restart: unless-stopped` の効果：

- Raspberry Pi本体が停電や再起動等でシャットダウンして立ち上がった際、Dockerデーモンの起動に伴ってコンテナが自動的に再始動します。
- 意図的に `docker compose stop` でコンテナを止めた場合を除き、プログラムのエラー等で強制終了した場合も自動的に復旧が試みられます。

### 3.2 ログのローテーション（推奨）

Raspberry PiのSDカードの寿命低下やディスク圧迫を防ぐため、コンテナのログサイズを制限することをおすすめします。必要に応じて、`/etc/docker/daemon.json` を以下のように設定するか、`docker-compose.yml` 内にログオプションを追加してください。

_docker-compose.yml への追記例（任意）_:

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### 3.3 コンテナの更新手順

最新のコードを取り込みたい場合のアップデート手順：

```bash
cd ~/withQ
git pull origin main
docker compose up -d --build
```

これで、新しいイメージのビルドおよびコンテナの再起動（ミリ秒単位のダウンタイム）がシームレスに行われます。
