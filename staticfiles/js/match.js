// CSRFトークンとゲームの初期データを読み込む。
// 初期データは、読み込み時のゲーム表示に使う。
const csrfToken = document.getElementById('csrf-data').dataset.csrf;

const initialMatchElement = document.getElementById('initial-match-data');
const matchId = initialMatchElement.dataset.matchId;
const initialTurn = initialMatchElement.dataset.initialTurn;
const initialBoard = JSON.parse(initialMatchElement.dataset.initialBoard);
const initialStatus = initialMatchElement.dataset.initialStatus;

// --- ターン管理: 表示と制御に関する処理 ---

//displayTurnIndicator()関数は、プレイヤーターン（黒か白）を表示する関数
//boardTurnは、'black\'s turn'か'white\'s turn'
const displayTurnIndicator = (boardTurn) => {
    const turnElement = document.getElementById('turn');
    if (boardTurn === 'black\'s turn') {
        turnElement.textContent = '黒'
    } else if (boardTurn === 'white\'s turn') {
        turnElement.textContent = '白'
    } else {
        turnElement.textContent = '不明'
    }
};

// 読み込み時に、ターンを表示する
displayTurnIndicator(initialTurn);

//パスボタンを押したときに、ターンを変更する関数
document.getElementById('pass-turn').addEventListener('click', async function (event) {
    try {
        const response = await fetch('/match/pass_turn/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,  // CSRFトークンをヘッダーに追加
            },
            body: JSON.stringify({ turn: 'passed', pk: matchId })
        });

        const data = await response.json();

        if (response.ok) {
            displayTurnIndicator(data.turn);
            console.log(`${data.message}`);
        } else {
            console.log(`Error: ${data.error}`);
        }
    } catch (error) {
        console.log(`Network error: ${error}`);
    }
});

//モデルのboard---各セルをblack, white, emptyで管理する---は1次元配列
//この2次元配列を1次元配列に変換する関数
const translateArray = (dim2_list) => {
    const dim1_list = []
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            dim1_list.push(dim2_list[i][j])
        }
    }
    return dim1_list
};

// const initialBoard = JSON.parse('{{ board|escapejs }}');  // board を JSON 文字列として埋め込む

console.log(initialBoard[3][4]);
const dim1InitialBoard = translateArray(initialBoard);
console.log(dim1InitialBoard);

for (let i = 0; i < 64; i++) {
    if (dim1InitialBoard[i] === 'black') {
        document.getElementById(`othello-cell${i}`).classList.add('black');
        document.getElementById(`othello-cell${i}`).classList.remove('white');
        document.getElementById(`othello-cell${i}`).classList.remove('empty');
    } else if (dim1InitialBoard[i] === 'white') {
        document.getElementById(`othello-cell${i}`).classList.add('white');
        document.getElementById(`othello-cell${i}`).classList.remove('black');
        document.getElementById(`othello-cell${i}`).classList.remove('empty');
    }
};

const updateBoard = (board) => {
    //引数boardはJSON文字列     
    //dim1Boardは、２次元のボードを１次元の配列にしたもの
    const dim1Board = translateArray(board);
    console.log(dim1Board);

    for (let i = 0; i < 64; i++) {
        if (dim1Board[i] === 'black') {
            document.getElementById(`othello-cell${i}`).classList.add('black');
            document.getElementById(`othello-cell${i}`).classList.remove('white');
            document.getElementById(`othello-cell${i}`).classList.remove('empty');
        } else if (dim1Board[i] === 'white') {
            document.getElementById(`othello-cell${i}`).classList.add('white');
            document.getElementById(`othello-cell${i}`).classList.remove('black');
            document.getElementById(`othello-cell${i}`).classList.remove('empty');
        }
    }
};

// result = { "blackCount": black_count, "whiteCount": white_count, "winner": winner, }
const displayGameResult = (result) => {
    const countResult = document.querySelector("#game-result .counts");
    const gameResult = document.querySelector("#game-result .result");
    countResult.innerHTML = `黒${result["blackCount"]}枚、白${result["whiteCount"]}枚。`
    if (result["winner"] === "black") {
        gameResult.innerHTML = `黒の勝ちです。`
    } else if (result["winner"] === "white") {
        gameResult.innerHTML = `白の勝ちです。`
    } else {
        gameResult.innerHTML = `引き分けです。`
    }
};

// ページ読み込み時に、対局が終了していたら、結果を表示する
if (initialStatus !== "対局中") {
    window.addEventListener("DOMContentLoaded", async function (event) {
        event.preventDefault();  // フォームのデフォルト動作を防止
        try {
            const response = await fetch('/match/end-game/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,  // CSRFトークンをヘッダーに追加
                },
                body: JSON.stringify({ pk: matchId })
            });

            const data = await response.json();

            if (response.ok) {
                displayGameResult(data);
                console.log(data);
            } else {
                console.log(`Error: ${data.error}`);
            }
        } catch (error) {
            console.log(`Network error: ${error}`);
        }
    });
}

//クリックして、オセロの駒を打つ処理
for (let i = 0; i < 64; i++) {
    document.getElementById(`othello-grid-item${i}`).addEventListener('click', async function (event) {
        event.preventDefault();  // フォームのデフォルト動作を防止

        const cell = i;
        const responseDiv = document.getElementById('response');


        try {
            const response = await fetch('/match/local/place-piece/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,  // CSRFトークンをヘッダーに追加
                },
                body: JSON.stringify({ cell: cell, pk: matchId })
            });

            const data = await response.json();

            if (response.ok) {
                //responseDiv.innerHTML = `<p>${data.message}</p>`;
                //const board = JSON.parse('{{ data.board|escapejs }}');  // fetch_data から返されたデータの board を使う
                updateBoard(data.board);
                displayTurnIndicator(data.turn);
            }
            else {
                responseDiv.innerHTML = `<p>Error: ${data.error}</p>`;
            }
        } catch (error) {
            responseDiv.innerHTML = `<p>Network error: ${error}</p>`;
        }
    });
};

// 終局処理
document.getElementById('end-game').addEventListener('click', async function (event) {
    event.preventDefault();  // フォームのデフォルト動作を防止
    const answer = confirm("本当にゲームを終了しますか？OKとすると、黒白それぞれの枚数を数えて、勝敗を決定します。");
    if (answer) {
        try {
            const response = await fetch('/match/end-game/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,  // CSRFトークンをヘッダーに追加
                },
                body: JSON.stringify({ pk: matchId })
            });

            const data = await response.json();

            if (response.ok) {
                displayGameResult(data);
                console.log(data);
            } else {
                console.log(`Error: ${data.error}`);
            }
        } catch (error) {
            console.log(`Network error: ${error}`);
        }
    }
});




console.log(typeof csrfToken)