document.addEventListener('DOMContentLoaded', _ => {
    const cardDiv = document.getElementById('card');
    const submitBtn = document.getElementById('submit-btn');
    const answerInput = document.getElementById('answer');
    const pk = JSON.parse(document.getElementById('deck-pk').textContent);

    let ws;

    function connect() {
        ws = new WebSocket(`ws://${location.host}/ws/reviews/${pk}/`);

        ws.addEventListener('message', event => {
            const data = JSON.parse(event.data);
            switch (data.type) {
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
});