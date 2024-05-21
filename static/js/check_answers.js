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

const checkAnswers = () => {
    const question = document.querySelector(".card-question");
    const questionId = question.dataset.questionId;
    const answers = document.querySelectorAll(".card-answer");

    for (const answer of answers) {

        answerId = answer.dataset.answerId;
        checkBox = answer.querySelector(".checkbox-field")

        checkBox.addEventListener("click", (event) => {
            event.preventDefault();
            const request = new Request(`/${questionId}/${answerId}/check_answer`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    isAuthor: true
                })
            })

            fetch(request)
                .then((response) => response.json())
                .then((data) => {
                    if (data.isAuthor === false) {
                        alert("You are not the author of this question");
                    } else {
                        checkBox.checked = !checkBox.checked;
                    }
                })
        })

    }

}


checkAnswers();