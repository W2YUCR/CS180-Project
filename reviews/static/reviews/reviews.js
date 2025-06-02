document.addEventListener('DOMContentLoaded', () => {
    const inner = document.getElementById('flip-card-inner');
    const frontFace = document.getElementById('card-front');
    const backFace = document.getElementById('card-back');
    const flipBtn = document.getElementById('flip-btn');
    const goodBtn = document.getElementById('good-btn');
    const againBtn = document.getElementById('again-btn');
    const deckPk = JSON.parse(document.getElementById('deck-pk').textContent);
    let ws;
    let expectingBack = false;
    let reviewEnded = false;
    function connect() {
        ws = new WebSocket(`ws://${location.host}/ws/reviews/${deckPk}/`);
        ws.addEventListener('open', () => { ws.send(JSON.stringify({ action: "ready" })); });
        ws.addEventListener('message', event => {
            const data = JSON.parse(event.data);
            switch (data.type) {
                case 'show':
                    if (expectingBack) {
                        backFace.textContent = data.card;
                        inner.classList.add('is-flipped');
                    } else {
                        inner.classList.remove('is-flipped');
                        frontFace.textContent = data.card;
                        backFace.textContent = '';
                    }
                    expectingBack = false;
                    reviewEnded = false;
                    break;
                case 'end':
                    frontFace.textContent = 'Review finished 🎉';
                    backFace.textContent = '';
                    inner.classList.remove('is-flipped');
                    reviewEnded = true;
                    break;
            }
        });
        ws.addEventListener('close', () => { setTimeout(connect, 0); });
    }
    connect();
    function flipLocally() {
        if (inner.classList.contains('is-flipped')) {
            inner.classList.remove('is-flipped');
            expectingBack = false;
        } else {
            ws.send(JSON.stringify({ action: "flip" }));
            expectingBack = true;
        }
    }
    document.getElementById('flip-card').addEventListener('click', () => {
        if (reviewEnded) {
            ws.send(JSON.stringify({ action: "ready" }));
        } else {
            flipLocally();
        }
    });
    flipBtn.addEventListener('click', () => {
        if (reviewEnded) {
            ws.send(JSON.stringify({ action: "ready" }));
        } else {
            flipLocally();
        }
    });
    goodBtn.addEventListener('click', () => {
        ws.send(JSON.stringify({ action: "rate", rating: "good" }));
        expectingBack = false;
    });
    againBtn.addEventListener('click', () => {
        ws.send(JSON.stringify({ action: "rate", rating: "again" }));
        expectingBack = false;
    });
});
