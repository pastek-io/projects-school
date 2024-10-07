const playerTurnLabel = document.getElementById("playerTurn");
const finalStateLabel = document.getElementById("finalState");
const tableGame = document.getElementById("tableGame");
const restartBtn = document.getElementById("restart-btn");
const NB_ROWS = 3;

let currentPlayer = 1
let winner = 0;
let playing = true;
let gamePanel = null;

initGame();

restartBtn.addEventListener("click", () => {
    initGame();
})

/**
 * Initialize / Restart the game 
 */
function initGame() {
    gamePanel = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ];

    winner = 0
    currentPlayer = currentPlayer;
    playing = true;

    playerTurn.innerText = currentPlayer == 1 ? "Player O " : "Player X";  
    finalStateLabel.innerText = ""
    restartBtn.style.display = "none"

    tableGame.innerHTML = createNodePanel(gamePanel);

    setTimeout(() => {        
        playerClickEvent()
    }, 300);
}

/**
 * Create the table node for the game panel
 * @param {Array} panel - game panel to show
 * @returns 
 */
function createNodePanel(panel) {
    let nodeTable = "";

    for (let row = 0; row < panel.length; row++) {
        nodeTable += `<tr>`;
        for (let col = 0; col < panel[row].length; col++) {
            let content = "";

            if (panel[row][col] !== 0) {                
                content = panel[row][col] == -1 ? "X" : "O";                
            }

            nodeTable += `<td data-pos="${row}-${col}">${content}</td>`;
        }
        nodeTable += `</tr>`;
    }

    return nodeTable;    
}

/**
 * Events for td to handle the process of the game
 */
function playerClickEvent() {
    if (playing) 
    {        
        let buttonsPlayable = document.querySelectorAll("td");
    
        for (const currentButton of buttonsPlayable) {
            if (currentButton.innerText === "") {
                
                currentButton.addEventListener("click", (e) => {
                    let pos = e.target.dataset.pos;
                    let posArray = pos.split("-");
                    let posX = -1;
                    let posY = -1;
    
                    posArray.forEach(pos => {
                        if (posX == -1) {
                            posX = parseInt(pos);
                        }
                        else 
                        {
                            posY = parseInt(pos);
                        }
                    });              
    
                    gamePanel[posX][posY] = currentPlayer;
    
                    tableGame.innerHTML = createNodePanel(gamePanel);
                
                    checkGameState();               

                    switchPlayerTurn();
                    
                    if (playing) {
                        setTimeout(() => { 
                            playerClickEvent();
                        }, 100);
                    }
                    else {  
                        showWinner();
                    }
                });
            }        
        }        
    }
}

function switchPlayerTurn() {
    currentPlayer = currentPlayer === 1 ? -1 : 1;
    playerTurn.innerText = currentPlayer == 1 ? "Player O " : "Player X";       
}

/**
 * Check for the stat eof the game panel -> if someone win / draw
 */
function checkGameState() {
    let panelIsFull = true;

    // Check if the panel is full -> DRAW
    for (const row of gamePanel) {
        if (row[0] === 0 || row[1] === 0 || row[2] === 0) {
            panelIsFull = false;
        }        

        if (!panelIsFull) {
            break;
        }
    }

    if (panelIsFull) {
        playing = false;                
    }
    else {
        // check rows to get a winner
        for (const row of gamePanel) {
            if (winner !== 0) {
                break;
            }
    
            if (row[0] + row[1] + row[2] === 3 || row[0] + row[1] + row[2] === -3) {
                winner = currentPlayer;
            }          
        }
    
        if (winner == 0) {
            // check cols to get a winner
            for (let colIndex = 0; colIndex < NB_ROWS; colIndex++) {
                if (winner !== 0) {
                    break;
                }
    
                if (gamePanel[0][colIndex] + gamePanel[1][colIndex] + gamePanel[2][colIndex] === 3 || gamePanel[0][colIndex] + gamePanel[1][colIndex] + gamePanel[2][colIndex] === -3) {
                    winner = currentPlayer;
                }            
            }
        }
    
        // check diagonal left -> right
        if (winner == 0 && (gamePanel[0][0] + gamePanel[1][1] + gamePanel[2][2] === 3 || gamePanel[0][0] + gamePanel[1][1] + gamePanel[2][2] === -3)) {
            winner = currentPlayer;
        }
    
        // check diagonal right -> left
        if (winner == 0 && (gamePanel[0][2] + gamePanel[1][1] + gamePanel[2][0] === 3 || gamePanel[0][2] + gamePanel[1][1] + gamePanel[2][0] === -3)) {
            winner = currentPlayer;
        }
        
        // Stop the game if someone win
        if (winner !== 0) {
            playing = false;
        }
    }

}

/**
 * Show the actual winner of the game or a draw message
 */
function showWinner() {
    if (winner == 0) 
    {
        finalStateLabel.style.color = "violet"; 
        finalStateLabel.innerText = "Draw !";  
    }
    else 
    {
        finalStateLabel.style.color = "lightgreen"; 
        finalStateLabel.innerText = winner == 1 ? "Player O win !" : "Player X win !";
    }

    restartBtn.style.display = "block"
}