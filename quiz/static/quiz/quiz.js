document.addEventListener('DOMContentLoaded', _ => {
    const cardDiv = document.getElementById('card');
    const cardCounter = document.getElementById('card-counter');
    const startBtn = document.getElementById('start-btn');
    const timer = document.getElementById('timer');
    const pk = JSON.parse(document.getElementById('quiz-pk').textContent);

    let ws;

    function displayCard(question) {
        cardDiv.innerText = question;
    }

    function displayAnswer(answer) {
        cardDiv.innerText = answer;
    }

    function endReview() {
        cardDiv.innerText = "Review finished.";
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
        setTimeout(() => setTimer(endTime), fractional);
    }

    function clearAndWaitForServer() {
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
                    endReview();
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
});