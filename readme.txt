// ターンの表示を変更
document.getElementById("turn").textContent = "白";
document.getElementById("turn").setAttribute("data-turn", "白");

<div data-user-id="123" data-user-name="John Doe" data-is-active="true">
  ユーザー情報
</div>

const element = document.querySelector('div');  // div要素を選択
const userId = element.dataset.userId;  // '123' が取得される
const userName = element.dataset.userName;  // 'John Doe' が取得される
const isActive = element.dataset.isActive;  // 'true' が取得される

document.getElementById("turn").textContent = "白";
document.getElementById("turn").setAttribute("data-turn", "白");