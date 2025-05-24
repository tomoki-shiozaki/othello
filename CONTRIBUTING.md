# Contributing Guide

このプロジェクトは現在、個人で開発・保守しています。将来的な他者参加も視野に入れ、開発ルールや環境構築手順をまとめています。

## 注意
- このドキュメントは自身の開発のための備忘録であり、かつ、草稿です。

## 環境構築

1. Python 3.12 を使用（推奨）
    - ユニットテストおよび統合テストは、Python 3.11、3.12、3.13 で実行しています。
2. 仮想環境の作成と有効化：

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows の場合: venv\Scripts\activate
    ```

3. 依存パッケージのインストール：

    ```bash
    pip install -r requirements.txt
    ```

4. 開発用サーバーの起動：

    ```bash
    python manage.py runserver
    ```

## コーディングスタイル・規約

### スタイルガイド

- Pythonのスタイルガイド [PEP8](https://peps.python.org/pep-0008/) に準拠してください。
- インデントはスペース4つ（タブ禁止）。
- 1行は最大79文字まで。
- コメントやdocstringはわかりやすく。
- 不要なimportは削除し、`isort`で整理。
- コード整形は`black`を使い、コミット前に必ず実行してください。

### 命名規則

- 変数名・関数名：`snake_case`（例: `total_price`）
- クラス名：`PascalCase`（例: `OrderItem`）
- 定数名：`UPPER_SNAKE_CASE`（例: `MAX_RETRY`）
- ファイル名：小文字スネークケース（例: `order_utils.py`）
- Djangoモデルのフィールドやメソッドも基本的に従うこと。

#### Django固有の命名ルール例

- **クラスベースビュー（CBV）**：  
  `モデル名 + 動詞 + View` で命名。モデル名は単数形を使う。    
  例：`BookCreateView`, `UserListView`

- **関数ベースビュー（FBV）**：  
  `動詞 + 対象` のスネークケース  
  例：`create_book`, `detail_article`, `list_user`, `edit_article`, `delete_article`

- **URL設計**：
  `名詞 + 動詞`。名詞（リソース）は複数形にする。    
  例：`/articles/`, `/articles/<id>/`, `/articles/create/`, `/articles/<id>/edit/`, `/articles/<id>/delete/`

- **URL名（name属性）**：  
  `名詞 + 状態`  
  例：`book_create`, `user_list`  
  もしくは、名前空間app_nameを使う（こちらを推奨）：  
  例：`app_name="articles"とし、name="list"`。他の場所では`articles:list`として参照

- **テンプレートファイル名**：  
  `モデル名（小文字） + アンダースコア + 動詞`  
  例：`book_form.html`, `article_list.html`, `article_create.html`, `article_delete.html`

- **テンプレート構成**：
  `アプリ名　＋　テンプレートファイル名`
  例：`articles/article_list.html`

  これらを守ることで、ファイルやクラスの役割が一目でわかりやすくなります。
- **アプリ名**：

  - **単数形**（概念やドメインを表す場合）：  
    例：`library`, `catalog`

  - **複数形や複合形**（複数ユーザー向けや複数のエンティティを含む場合）：  
    例：`accounts`, `user_libraries`, `posts`

  プロジェクト全体で統一した形式を採用し、一貫性を保つことが重要です。

### 静的解析ツール

- [flake8](https://flake8.pycqa.org/) を使用し、コードの問題を検出。
- 以下のコマンドでチェック可能：

```bash
black .
isort .
flake8 .
```

### コード例：
```python
def calculate_total(price: float, tax_rate: float) -> float:
    """
    商品価格に税率を掛けて税込価格を計算します。

    Args:
        price (float): 商品価格
        tax_rate (float): 税率（例: 0.08）

    Returns:
        float: 税込価格
    """
    return price * (1 + tax_rate)
```

## ブランチ運用

- 基本ブランチ: main

- 機能追加や修正の際はブランチを作成
    - feature/〇〇: 機能追加  
    - bugfix/〇〇: バグ修正  
    - refactor/〇〇: リファクタリング  

## コミットメッセージルール（任意）
以下のようなフォーマットを意識してください。
- feat: 新機能の追加
- fix: バグの修正
- refactor: コードの整理
- docs: ドキュメントの更新

## テスト実行

- ユニットテストおよび統合テストは、Python 3.11、3.12、3.13 の環境で実行されます。
- テストを実行するには以下のコマンドを使用します：

    ```bash
    python manage.py test
    ```

  ※ pytest や coverage を使用している場合は、適宜追記してください。

## その他の注意点
- .env ファイルはリポジトリに含めず、.env.example を用意してください。
- 機密情報や秘密鍵は含めないでください。
- 必要に応じて README.md と併用してください。

このガイドは自身の開発効率と継続性のための備忘録です。
将来的に他の開発者の参加がある場合は内容を拡充・更新していきます。