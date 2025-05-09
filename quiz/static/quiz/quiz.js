document.addEventListener('DOMContentLoaded', _ => {
    const cardDiv = document.getElementById('card');
    const cardCounter = document.getElementById('card-counter');
    const startBtn = document.getElementById('start-btn');
    const submitBtn = document.getElementById('submit-btn');
    const answerInput = document.getElementById('answer');
    const timer = document.getElementById('timer');
    const pk = JSON.parse(document.getElementById('quiz-pk').textContent);

    let ws;

    function displayCard(question) {
        cardDiv.innerText = question;
        answerInput.value = '';
        answerInput.disabled = false;
    }

    function displayAnswer(answer) {
        cardDiv.innerText = answer;
    }

    function endReview(score) {
        cardDiv.innerText = `Review finished. Score: ${score}`;
    }

    let timerTimout;

    function setTimer(endTime) {
        const now = Date.now();
        const delta = endTime - now;
        const secs = Math.ceil(delta / 1000);
        timer.innerText = secs.toString();
        if (secs <= 0) {
            clearAndWaitForServer();
            return;
        }
        const fractional = delta % 1000;
        timerTimout = setTimeout(() => setTimer(endTime), fractional);
    }

    function clearAndWaitForServer() {
        clearTimeout(timerTimout);
        answerInput.disabled = true;
        cardDiv.innerText = "";
    }

    window.setTimer = setTimer;
    function connect() {
        ws = new WebSocket(`ws://${location.host}/ws/quiz/${pk}/`);

        ws.addEventListener('message', event => {
            const data = JSON.parse(event.data);
            switch (data.type) {
                case 'timeout':
                    displayAnswer(data.answer);
                    break;

                case 'show':
                    startBtn.remove();
                    displayCard(data.question);
                    setTimer(data.end_time);
                    break;
                case 'end':
                    endReview(data.score);
                    break
                default:
                    break;
            }
        });

        ws.addEventListener('close', _ => {
            setTimeout(connect, 0);
        });
    }

    connect();

    startBtn.addEventListener('click', _ => {
        ws.send(JSON.stringify({ action: 'start' }));
    });

    submitBtn.addEventListener('click', _ => {
        ws.send(JSON.stringify({
            action: 'answer',
            answer: answerInput.value,
        }));
        clearAndWaitForServer();
    })
});