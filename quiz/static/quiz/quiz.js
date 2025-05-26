document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-btn');
    const submitBtn = document.getElementById('submit-btn');
    const answerInput = document.getElementById('answer');
    const cardDiv = document.getElementById('card');
    const cardCounter = document.getElementById('card-counter');
    const timer = document.getElementById('timer');
    const pk = JSON.parse(document.getElementById('quiz-pk').textContent);

    // 🔒 Ensure submit is disabled initially
    submitBtn.disabled = true;
    answerInput.disabled = true;

    let ws;
    let timerTimeout;
    let currentCardIndex = 0;

    function displayCard(question) {
        cardDiv.innerText = question;
        answerInput.value = '';
        answerInput.disabled = false;
        submitBtn.disabled = false;
        currentCardIndex++;
        cardCounter.innerText = currentCardIndex;
    }

    function displayAnswer(answer) {
        cardDiv.innerText = answer;
    }

    function endReview(score) {
        cardDiv.innerText = `Review finished. Score: ${score}`;
        submitBtn.disabled = true;
        answerInput.disabled = true;
    }

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
        timerTimeout = setTimeout(() => setTimer(endTime), fractional);
    }

    function clearAndWaitForServer() {
        clearTimeout(timerTimeout);
        submitBtn.disabled = true;
        answerInput.disabled = true;
        cardDiv.innerText = '';
    }

    function connect() {
        ws = new WebSocket(`ws://${location.host}/ws/quiz/${pk}/`);

        ws.addEventListener('message', event => {
            const data = JSON.parse(event.data);
            switch (data.type) {
                case 'timeout':
                    displayAnswer(data.answer);
                    submitBtn.disabled = true;
                    break;

                case 'show':
                    startBtn.style.display = 'none';
                    displayCard(data.question);
                    setTimer(data.end_time);
                    break;

                case 'end':
                    endReview(data.score);
                    break;
            }
        });

        ws.addEventListener('close', () => {
            setTimeout(connect, 1000);
        });
    }

    connect();

    startBtn.addEventListener('click', () => {
        ws.send(JSON.stringify({ action: 'start' }));
    });

    submitBtn.addEventListener('click', () => {
        submitBtn.disabled = true; // 🔒 prevent double-submit
        ws.send(JSON.stringify({
            action: 'answer',
            answer: answerInput.value,
        }));
        clearAndWaitForServer();
    });
});
