# オセロWebアプリ

## 概要
オセロアプリをDjangoで開発しています。現在(2025年5月30日)はローカル対戦機能を実装済みです。

## 目的
このプロジェクトは、以下を目的として開発しました：

- Djangoの実践的な開発スキルを習得する
- ロジック性の高いゲームを通して、設計・データ管理の経験を深める
- フロントエンドとバックエンドの連携を一通り経験する
- デプロイやユーザー管理、パーミッションなど、Webアプリ全体の構成を学ぶ

## 開発ドキュメント
- 開発ドキュメントは[こちら](docs/README.md)をご覧ください。

## 機能一覧
- ローカル対戦(同一画面で2人対戦)

## 使用技術

| 分類         | 技術                                      |
|--------------|-------------------------------------------|
| バックエンド | Django                                    |
| フロントエンド | HTML / CSS / JavaScript / Bootstrap       |
| データベース | SQLite（開発環境） / PostgreSQL（本番環境） |

## 画面イメージ
![ゲーム画面(2025/04/27)](docs/images/game_image_v0.2.0.png)

## 必要な環境・依存関係
- **Pythonバージョン**: 3.12（動作確認済み）
- **依存ライブラリ**:
  - Django 5.1.7

## セットアップ手順

  ```bash
  # `pipenv`で必要なライブラリをインストールします。
  pipenv install
  # 仮想環境を起動します。
  pipenv shell
  # マイグレーションを行います。
  python manage.py migrate
  # ローカルサーバーを起動します。
  python manage.py runserver
  # その後、ブラウザで`http://127.0.0.1:8000/`にアクセスしてください。
  ```
    

## 使用方法
`http://127.0.0.1:8000/`にアクセスしてください。基本的な操作は、アプリ画面上の指示に従って進めることができます。

## テスト方法

次のコマンドを実行して、テストを行ってください。
  ```bash
  python manage.py test
  ```

## デプロイ
- RenderとNeonでデプロイしています。
- 本番環境（mainブランチ）URL:  
  [https://othello-main.onrender.com/](https://othello-main.onrender.com/)

- 過去バージョンのデプロイURL:  
  - v1.0.0のURL: [https://othello-d46f.onrender.com/](https://othello-d46f.onrender.com
  )  
  - v2.0.0のURL: [https://othello-feature-guest-user-play.onrender.com/](https://othello-feature-guest-user-play.onrender.com/)

- 機能開発用プレビュー環境（feature/guest-user-playブランチ）URL:  
  [https://othello-feature-guest-user-play.onrender.com/](https://othello-feature-guest-user-play.onrender.com/)

- システム構成図は以下の通りで、アプリ全体の構成を簡潔に示しています。
##### システム構成図

![システム構成図](docs/system_architecture/system_architecture/system_architecture.svg)