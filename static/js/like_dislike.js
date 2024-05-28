function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const like = () => {
    const questions = document.querySelectorAll(".card-question");

    for (const question of questions) {

        const questionId = question.dataset.questionId;
        const likeButton = question.querySelector(".button-like");
        const likeCounter = question.querySelector(".like-counter");
        const dislikeButton = question.querySelector(".button-dislike");
        const dislikeCounter = question.querySelector(".dislike-counter");

        likeButton.addEventListener("click", () => {
            const request = new Request(`/${questionId}/like_question`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    pressedLike: true
                })
            })

            fetch(request)
                .then((response) => response.json())
                .then((data) => {
                    likeCounter.innerHTML = data.likes_count;
                    dislikeCounter.innerHTML = data.dislikes_count;
                })
        })

        dislikeButton.addEventListener("click", () => {
            const request = new Request(`/${questionId}/like_question`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    pressedLike: false
                })
            })

            fetch(request)
                .then((response) => response.json())
                .then((data) => {
                    likeCounter.innerHTML = data.likes_count;
                    dislikeCounter.innerHTML = data.dislikes_count;
                })
        })

    }
}

const likeAnswer = () => {
    const answers = document.querySelectorAll(".card-answer");

    for(const answer of answers) {

        const answerId = answer.dataset.answerId;
        const likeButton = answer.querySelector(".button-like");
        const likeCounter = answer.querySelector(".like-counter");
        const dislikeButton = answer.querySelector(".button-dislike");
        const dislikeCounter = answer.querySelector(".dislike-counter");

        likeButton.addEventListener("click", () => {
            const request = new Request(`/${answerId}/like_answer`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    pressedLike: true
                })
            })

            fetch(request)
                .then((response) => response.json())
                .then((data) => {
                    likeCounter.innerHTML = data.likes_count;
                    dislikeCounter.innerHTML = data.dislikes_count;
                })
        })

        dislikeButton.addEventListener("click", () => {
            const request = new Request(`/${answerId}/like_answer`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    pressedLike: false
                })
            })

            fetch(request)
                .then((response) => response.json())
                .then((data) => {
                    likeCounter.innerHTML = data.likes_count;
                    dislikeCounter.innerHTML = data.dislikes_count;
                })
        })

    }
}

like();
likeAnswer();