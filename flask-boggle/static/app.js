class BoggleGame {
    
    constructor(seconds = 60) {
        this.seconds = seconds;
        this.score = 0;
        this.words = new Set();
        this.guesses = 0;

        
        $("#submit-guess").on("click", this.handleGuess.bind(this));
      
        this.timer = setInterval(this.count.bind(this), 1000);
    }



 
    async handleGuess(evt) {

        evt.preventDefault();
   
        const $wordInput = $("#word-guessed")
        
        const word = $wordInput.val().toLowerCase();

       
        if (!word) return;

        
        this.guesses++;
        
        if (this.words.has(word)) {
   
            this.displayWords(word, "bad");
            this.displayMessage(`You already found "${word}"`, "bad-msg");
            return;
        }

        
        const response = await axios.get(`/check-guess`, { params: { word } });

        if (response.data.result === "not-word") {

            this.displayWords(word, "bad");
 
            this.displayMessage(`${word} is not a valid word`, "bad-msg");
        } else if (response.data.result === "not-on-board") {

            this.displayWords(word, "bad");
      
            this.displayMessage(`<p><span>${word.toUpperCase()}</span> is not on the board!</p>`, "bad-msg");
        } else {

            this.displayWords(word, "good");
 
            this.displayMessage(`Nice! Good word, keep going!`, "good-msg");
      
            this.score += word.length;

            this.displayScore();
       
            this.words.add(word);
        }
       
        $wordInput.val("");
    }



    async handleScore() {
        
        const response = await axios.post(`/post-score`, { score: this.score });
       
        if(response.data.broke_record) {
            alert(`You got the new High Score: ${response.data.highscore}`)
            this.displayMessage(`You Got the New High Score: ${response.data.highscore}!`, "good-msg");
            $("#highscore").text(response.data.highscore);
        }
       
    }



    count() {
    
        this.seconds -= 1;

        this.displayTimer();
       
        if (this.seconds === 0) {
           
            alert("Times Up!");
           
            this.displayMessage(`Times Up!`, "");
            
            clearInterval(this.timer);
       
            $("#submit-guess").attr("disabled", true);

 
            this.handleScore();
        }
    }




    displayTimer() {
        $("#timer").text(this.seconds);
    }



    displayMessage(msg, cls) {
       
        $("#message").text("")
 
        $("#message").append(msg);
        
        $("#message").removeClass("bad-msg good-msg").addClass(cls); 

        if (cls === "bad-msg")
            setTimeout(function () {
                $("#message").text("")
                $("#message").append(`<p>Keep Guessing</p>`);
            }, 2000);
    }



   
    displayScore() {
        $("#score").text(this.score);
    }



    displayWords(word, cls) {

        const points = cls === "good" ? word.length : 0;

      
        const wordMarkUp = `
        <tr>
            <th scope="row">${this.guesses}</th>
            <td class="${cls}">${word}</td>
            <td class="${cls}">${points}</td>
        </tr>`
        
        $("#words").append(wordMarkUp)

    }
}