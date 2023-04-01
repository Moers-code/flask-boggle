

let word = '';
let score = 0;
let wordSet = new Set();

// Make calls to server to validate word
const serverRequest = async () => {
    let data = {playerGuess: word}
    try {
        const res = await axios.post('/guess', data);
        return res.data.result
    } catch(err){
        console.log(err);
    }
}

// UI: Displays Score
const displayScore = () => {
    score = 0;
    for(str of wordSet){
        score += str.length
    }
    $("#score").text(score)
}

// UI: Displays Score
const displayWords = () =>{
    $("ul").empty()
    for (val of wordSet){
        $("ul").append(`<li>${val}</li>`)
    }
}

// Callback: verifies if word
const handleForm = async (e) => {
    e.preventDefault();
    const result = await serverRequest();

    if(result === "ok"){
        wordSet.add(word)
    }  
    
    displayWords();
    displayScore();
    word = '';
}


const startGame = () => {
    let timeLeft = 20
    let gameTimer = setInterval(async() => {
        timeLeft--;
        $("#timer").text(timeLeft);
        if(timeLeft === 0){
            clearInterval(gameTimer);
    
            try{
                let res = await axios.post('/update_score', {score: score})
                window.location.href = '/score';
            }catch(err){
                console.log(err)
            }
        }
    }, 1000)

    $('td').on('click', (e) => {
        word += $(e.target).attr("id");
    })
    
    $("#check-word-button").on('click', handleForm);
}


startGame();



