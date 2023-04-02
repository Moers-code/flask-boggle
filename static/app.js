const BASE_URL = "http://127.0.0.1:5000/play_game/"

class Game{
    constructor(){
        this.word = '';
        this.score = 0;
        this.wordSet = new Set();
    }

    // Make calls to server to validate word
    serverRequest = async () => {
        if (this.word === '' || this.word === null || this.word.length < 2) return;
        let data = {playerGuess: this.word}
        try {
            const res = await axios.post('/guess', data);
            return res.data.result
        } catch(err){
            console.log(err);
        }
    }

    calcScore = () => {
        this.score = 0;
        for(this.str of this.wordSet){
            this.score += this.str.length;
        }
    }

    // UI: Displays Score
    displayScore = () => {
        this.calcScore();
        $("#score").text(this.score)
    }
    // UI: Displays Score
    displayWords = () =>{
        $("ul").empty();
        for (this.val of this.wordSet){
            $("ul").append(`<li>${this.val}</li>`)
        }
    }

    // Callback: verifies if word
    handleForm = async (e) => {
        e.preventDefault();
        const result = await this.serverRequest();

        if(result === "ok"){
            this.wordSet.add(this.word)
        }  
        this.displayWords();
        this.displayScore();
        $('td').removeClass('clicked');
        this.word = '';
    }

    startGame = () => {
    
        let timeLeft = 60
        let gameTimer = setInterval(async() => {
            timeLeft--;
            $("#timer").text(timeLeft);
            if(timeLeft === 0){
                clearInterval(gameTimer);
                try{
                    let res = await axios.post('/update_score', {score: this.score})
                    window.location.href = '/score';
                }catch(err){
                    console.log(err)
                }
            }
        }, 1000)
        
        // Event Listener for Letters Choice
        $('td').on('click', (e) => {
            this.word += $(e.target).attr("class");
            $(e.target).toggleClass('clicked');
        }) 

        // Event Listener for Word Validation
        $("#guess-form").on('submit', this.handleForm);   
    }
}

$(document).ready(function() {
    if (window.location.href === BASE_URL) {
      // if the url for /play_game is loaded, start game & timer
        const newBoggle = new Game();
        newBoggle.startGame();
    }
  });