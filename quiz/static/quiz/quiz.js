const csrftoken = Cookies.get('csrftoken');
document.addEventListener('DOMContentLoaded', _ => {
    const cardDiv = document.getElementById('card');
    const knownBtn = document.getElementById('known-btn');
    const unknownBtn = document.getElementById('unknown-btn');
    const nextBtn = document.getElementById('next-btn');
    const cardCounter = document.getElementById('card-counter');

    async function load() {
        const response = await fetch('./current');
        const data = await response.json();
        if (data['finished']) {
            cardDiv.textContent = 'Finished reviewing';
        }
        else {
            cardDiv.textContent = data['front'];
            cardCounter.innerText = data['index'] + 1;
        }
    }

    knownBtn.addEventListener('click', async _ => {
        const response = await fetch('./current');
        const data = await response.json();
        cardDiv.textContent = data['back'];
    });

    unknownBtn.addEventListener('click', async _ => {
        const response = await fetch('./current');
        const data = await response.json();
        cardDiv.textContent = data['back'];
    });

    nextBtn.addEventListener('click', async _ => {
        await fetch('./next', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'X-CSRFToken': csrftoken
            },
        });
        await load();
    });

    load();
});