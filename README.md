# オセロ Web アプリ

[![Build Status](https://github.com/tomoki-shiozaki/othello/actions/workflows/ci.yml/badge.svg)](https://github.com/tomoki-shiozaki/othello/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/tomoki-shiozaki/othello/graph/badge.svg?token=W0PHF5YR7Z)](https://codecov.io/gh/tomoki-shiozaki/othello)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 概要

オセロアプリを Django で開発しました。ローカル対戦機能を実装済みです。  
本番環境は [こちら](https://othello-main.onrender.com/) でデプロイされており、実際にブラウザ上でプレイ可能です。

> ＊ただし、現在は Render の無料プランを使用しているため、最初の起動には約 1 分程度の待機時間が発生することがあります。ご了承ください。
> 私の他の成果物である [図書館アプリ](https://github.com/tomoki-shiozaki/distributed-library) は Cloud Run でデプロイしており、起動が約 10 秒程度で行えます。

ログインせずにゲストユーザーとしてプレイすることも可能ですが、[テスト用アカウント](#テスト用アカウント)を用いると、すべての機能が利用できます。

## 目的

このプロジェクトは、以下を目的として開発しました：

- Django の実践的な開発スキルを習得する
- ロジック性の高いゲームを通して、設計・データ管理の経験を深める
- フロントエンドとバックエンドの連携を一通り経験する
- デプロイやユーザー管理、パーミッションなど、Web アプリ全体の構成を学ぶ

## 技術的な工夫

- Django のセッション管理を利用し、ログインなしでゲストユーザーとしてプレイ可能にしています。
- さらに、アカウント登録をすると、対局の保存・再開や過去の対局履歴の確認などの機能も利用可能です。

## 開発ドキュメント

- 開発ドキュメントは[こちら](docs/README.md)をご覧ください。

## 機能一覧

- ローカル対戦(同一画面で 2 人対戦)

## 使用技術

| 分類           | 技術                                        |
| -------------- | ------------------------------------------- |
| バックエンド   | Django                                      |
| フロントエンド | HTML / CSS / JavaScript / Bootstrap         |
| データベース   | SQLite（開発環境） / PostgreSQL（本番環境） |

## 画面イメージ

![ゲーム画面(2025/04/27)](docs/images/game_image_v0.2.0.png)

## 必要な環境・依存関係

- **Python バージョン**: 3.12（動作確認済み）
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

- Render と Neon でデプロイしています。
- Render の無料プランを使っており、スリープ状態からの起動に約 1 分かかる場合があります。
- 快適な利用のため、今後 Cloud Run でのデプロイも検討しています。  
  私の他の成果物である [図書館アプリ](https://github.com/tomoki-shiozaki/distributed-library) では、  
  実際の業務を意識して Cloud Run でのデプロイや CI/CD を用いた運用を行っています。

- 本番環境（main ブランチ）URL:  
  [https://othello-main.onrender.com/](https://othello-main.onrender.com/)

- 過去バージョンのデプロイ URL:

  - v1.0.0 の URL: [https://othello-d46f.onrender.com/](https://othello-d46f.onrender.com)
  - v2.0.0 の URL: [https://othello-feature-guest-user-play.onrender.com/](https://othello-feature-guest-user-play.onrender.com/)

- 機能開発用プレビュー環境（feature/guest-user-play ブランチ）URL:  
  [https://othello-feature-guest-user-play.onrender.com/](https://othello-feature-guest-user-play.onrender.com/)

- システム構成図は以下の通りで、アプリ全体の構成を簡潔に示しています。

##### システム構成図

![システム構成図](docs/system_architecture/system_architecture/system_architecture.svg)

## テスト用アカウント

テスト用アカウントを使用することで、すべての機能を試すことができます。ログイン後、以下の追加機能が利用可能です：

- 対局履歴の保存と再開
- 過去の対局履歴の確認

テスト用アカウント:

- ユーザー名: `user1`
- パスワード: `dev_user1_123`

ゲストプレイでも基本的な対局は可能ですが、アカウント作成後の機能もぜひお試しください。

## ライセンス

このプロジェクトは [MIT ライセンス](LICENSE) のもとで公開されています。

## 作者 / Author

塩崎 友貴 (Tomoki Shiozaki)  
[GitHub アカウント](https://github.com/tomoki-shiozaki)
