function submit_message() {
  const form = document.getElementById('mainForm');
  const chatbox = document.getElementById('chatbox');

  const formData = new FormData(form);
  const formObject = {};

  formData.forEach((value, key) => {
    formObject[key] = value;
  });

  const url = `http://127.0.0.1:8000/chat/${GUID}`;
  const headers = new Headers();
  headers.append('Content-Type', 'application/json');

  document.getElementById('loading-wrapper').style.display = 'block';
  document.body.style.overflow = 'hidden';

  // save the message from the form into a JSON string
  const body = JSON.stringify(formObject);

  // clear the form textarea input
  document.getElementById("chatbot-input").value = "";
  // append the message to the chat history
  chatbox.insertAdjacentHTML('beforeend', `<div class="user">${formObject["message"]}</div>`);

  // scroll to bottom of chat
  chatbox.scrollTo({
    top: chatbox.scrollHeight - chatbox.clientHeight,
    behavior: 'smooth'
  });

  fetch(url, {
    method: 'POST',
    headers: headers,
    body: body,
  })
    .then(response => {
      const reader = response.body.getReader();
      return new ReadableStream({
        start(controller) {
          function push() {
            reader.read().then(({ done, value }) => {
              if (done) {
                console.log('Stream complete');
                controller.close();
                return;
              }
              // Assuming value is Uint8Array or ArrayBuffer, convert to text
              const text = new TextDecoder().decode(value);
              console.log('Received chunk:', text);
              // Append chunk to chatbox
              chatbox.insertAdjacentHTML('beforeend', text);
              // scroll to bottom of chat
              chatbox.scrollTo({
                top: chatbox.scrollHeight - chatbox.clientHeight,
                behavior: 'smooth'
              });
              push(); // Continue reading
            }).catch(error => {
              console.error('Error reading stream:', error);
              controller.error(error);
            });
          }
          push();
        }
      });
    })
    .then(stream => {
      // Do something with the stream if needed
    })
    .catch(error => {
      console.error('Fetch error:', error);
      document.getElementById('response').innerText = 'Fetch error: ' + error;
    })
    .finally(() => {
      // hide the loading wrapper
      document.getElementById('loading-wrapper').style.display = 'none';
      document.body.style.overflow = 'auto';

      // scroll to bottom of chat
      chatbox.scrollTo({
        top: chatbox.scrollHeight - chatbox.clientHeight,
        behavior: 'smooth'
      });
    });
}

document.getElementById('chatbot-input').addEventListener('keydown', function (event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault(); // Prevent default behavior (new line)
    submit_message(); // Submit the form
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('mainForm');

  form.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    submit_message();
  });

  const chatbox = document.getElementById('chatbox');
  // scroll to bottom of chat
  chatbox.scrollTo({
    top: chatbox.scrollHeight - chatbox.clientHeight,
    behavior: 'smooth'
  });
});