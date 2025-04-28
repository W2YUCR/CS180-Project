document.addEventListener('DOMContentLoaded', _ => {
    const cardDiv = document.getElementById('card');
    const knownBtn = document.getElementById('known-btn');
    const unknownBtn = document.getElementById('unknown-btn');
    const nextBtn = document.getElementById('next-btn');
    const cardCounter = document.getElementById('card-counter');
    const pk = JSON.parse(document.getElementById('quiz-pk').textContent)

    var ws = new WebSocket(`ws://${location.host}/ws/quiz/${pk}/`)
});