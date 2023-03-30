let guess = '';

$('td').on('click', (e) => {
    guess += $(e.target).attr("id");
    console.log(guess)
})





const handleForm = async (e) => {
    e.preventDefault();
    let data = {playerGuess: guess}
    
    try {
        const res = await axios.post('/guess', data);
        console.log(res);
    } catch(err){
        console.log(err)
    }
    guess = '';
}

$("#check-word-button").on('click', handleForm);




