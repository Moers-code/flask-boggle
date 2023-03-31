console.log("JavaScript code is executing on the redirected page.");
let word = '';
let score = 0;


const serverRequest = async () => {
    let data = {playerGuess: word}
    try {
        const res = await axios.post('/guess', data);
        return res.data.result
    } catch(err){
        console.log(err);
    }
}

const displayScore = () => {
    $("#score").text(score)
    
}

const displayWords = (val) =>{
    $("ul").append(`<li>${val}</li>`)
}


const handleForm = async (e) => {
    e.preventDefault();
    const result = await serverRequest();
    if(result === "ok"){
        displayWords(word);
        score += (word).length;
    }
    displayScore();
    
    word = '';
}


const startGame = () => {
    
    let gameTimer = setTimeout(async() => {
        let data = {score: score};
     
        try{
            let res = await axios.post('/update_score', data)
            window.location.href = '/score';
        }catch(err){
            console.log(err)
        }
        
        clearTimeout(gameTimer)
    }, 20000)

    $("#timer").text(gameTimer);

    $('td').on('click', (e) => {
        word += $(e.target).attr("id");
    })
    
    $("#check-word-button").on('click', handleForm);
}


startGame();



