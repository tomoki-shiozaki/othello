# UI 設計書

## G001: ホーム画面

- **概要**: ユーザーが一番最初にアクセスする画面。ユーザーアカウント関連の機能、対戦選択を扱う。
- **構成要素**:
  - ローカル対戦ボタン
  - リモート対戦ボタン
  - ユーザーアカウントボタン
- **操作**:
  - ローカル対戦ボタンを押すと、ローカル対戦画面（G002）に遷移
  - リモート対戦ボタンを押すと、リモート対戦待合画面（G003）に遷移
  - ログインボタンを押すと、ログイン画面に遷移
  - ログアウトボタンを押すと、ログアウト画面に遷移
- **遷移先**:
  - ローカル対戦 → G002
  - リモート対戦 → G003
  - ログアウト → ログイン画面

---

## G002: ローカル対戦画面