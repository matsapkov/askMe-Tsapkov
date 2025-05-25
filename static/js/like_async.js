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

document.querySelectorAll('button[data-question-id]').forEach(btn => {
    btn.addEventListener('click', async e => {
        e.preventDefault();
        const qid = btn.dataset.questionId;
        const url = `/question/${qid}/like_async/`;

        try {
            const res = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);

            const data = await res.json();

            const counter = document.querySelector(`span[data-like-counter="${qid}"]`);
            counter.textContent = data.likes_count;

            const heart = btn.querySelector('.heart');
            if (data.liked) {
                btn.classList.replace('btn-outline-secondary', 'btn-danger');
                heart.textContent = '❤';
            } else {
                btn.classList.replace('btn-danger', 'btn-outline-secondary');
                heart.textContent = '🤍';
            }

        } catch (err) {
            console.error('Like toggle failed:', err);
        }
    });
});
