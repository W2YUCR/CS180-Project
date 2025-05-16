document.addEventListener('DOMContentLoaded', _ => {
    const cardDiv = document.getElementById('card');
    const flipBtn = document.getElementById('flip-btn');
    const goodBtn = document.getElementById('good-btn');
    const againBtn = document.getElementById('again-btn');
    const answerInput = document.getElementById('answer');
    const pk = JSON.parse(document.getElementById('deck-pk').textContent);

    let ws;

    function displayCard(question) {
        cardDiv.innerText = question;
        answerInput.value = '';
        answerInput.disabled = false;
    }

    function endReview() {
        cardDiv.innerText = `Review finished.`;
    }

    function connect() {
        ws = new WebSocket(`ws://${location.host}/ws/reviews/${pk}/`);

        ws.addEventListener('open', _ => {
            ws.send(JSON.stringify({ action: "ready" }))
        });

        ws.addEventListener('message', event => {
            const data = JSON.parse(event.data);
            switch (data.type) {
                case 'show':
                    displayCard(data.card);
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

    flipBtn.addEventListener('click', _ => {
        ws.send(JSON.stringify({ action: "flip" }))
    });

    goodBtn.addEventListener('click', _ => {
        ws.send(JSON.stringify({ action: "rate", rating: "good" }))
    });

    againBtn.addEventListener('click', _ => {
        ws.send(JSON.stringify({ action: "rate", rating: "again" }))
    });
});