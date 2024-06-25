document.getElementById('model').addEventListener('change', function () {
    document.getElementById('settingsResponse').innerText = '';
    if (this.value === 'gpt-3.5-turbo') {
        document.getElementById('openai-fields').style.display = 'block';
        document.getElementById('api-token').setAttribute('required', '');
    } else {
        document.getElementById('openai-fields').style.display = 'none';
        document.getElementById('api-token').inputField.removeAttribute('required');
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('settingsForm');

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);
        const formObject = {};

        formData.forEach((value, key) => {
            formObject[key] = value;
        });

        fetch(`http://127.0.0.1:8000/settings/${GUID}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formObject),
        })
            .then(response => response.json()) // Expecting JSON response
            .then(data => {
                console.error('Response: ', data.response);
                document.getElementById('settingsResponse').innerText = data.response;
            })
            .catch(error => {
                console.error('Error: ', error);
                document.getElementById('settingsResponse').innerText = 'Error: ' + error;
            });
    });
});