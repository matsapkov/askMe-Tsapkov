function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookieString => {
            const cookie = cookieString.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
            }
        });
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

document.getElementById('answers-container').addEventListener('change', async function (e) {
    if (!e.target.matches('input.correct-checkbox[data-answer-id]')) return;

    const cb = e.target;
    const aid = cb.dataset.answerId;
    const url = `/answer/${aid}/answer_like_async/`;

    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin'
    });

    const data = await res.json();
    const counter = document.querySelector(`[data-correct-counter="${aid}"]`);
    if (counter) {
        counter.innerText = data.likes_count;
    }
});
