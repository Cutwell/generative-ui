document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('mainForm');
    const chatbox = document.getElementById('chatbox')

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);
        const formObject = {};

        formData.forEach((value, key) => {
            formObject[key] = value;
        });

        fetch(`http://127.0.0.1:8000/chat/${GUID}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formObject),
        })
            .then(response => response.json()) // Expecting JSON response
            .then(data => {
                chatbox.insertAdjacentHTML('beforeend', data.content);
                const spinnerWrapper = document.querySelector('#loading-wrapper')
                spinnerWrapper.style.display = 'none';
                document.body.style.overflow = 'auto';
                chatbox.scrollTo({
                    top: chatbox.scrollHeight - chatbox.clientHeight,
                    behavior: 'smooth'
                });
            })
            .catch(error => {
                console.error('Error: ', error);
                document.getElementById('response').innerText = 'Error: ' + error;
                chatbox.scrollTo({
                    top: chatbox.scrollHeight - chatbox.clientHeight,
                    behavior: 'smooth'
                });
            });
    });
});