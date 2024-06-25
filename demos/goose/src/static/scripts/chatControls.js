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

  // Save the message from the form into a JSON string
  const body = JSON.stringify(formObject);

  // Clear the form textarea input
  document.getElementById("chatbot-input").value = "";
  // Append the message to the chat history
  chatbox.insertAdjacentHTML('beforeend', `<div class="user">${formObject["message"]}</div>`);
  // Create a new div for the server response
  const responseDiv = document.createElement('div');
  responseDiv.classList.add('response');
  chatbox.appendChild(responseDiv);

  // Scroll to bottom of chat
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
      const decoder = new TextDecoder();
      let buffer = '';

      return new ReadableStream({
        start(controller) {
          function push() {
            reader.read().then(({ done, value }) => {
              if (done) {
                if (buffer) {
                  //responseDiv.innerHTML += buffer;
                  chatbox.scrollTo({
                    top: chatbox.scrollHeight - chatbox.clientHeight,
                    behavior: 'smooth'
                  });
                }
                console.log('Stream complete');
                controller.close();
                return;
              }
              // Decode and append the chunk to the buffer
              buffer += decoder.decode(value, { stream: true });

              // Update the response div with the accumulated buffer
              responseDiv.innerHTML = buffer;
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
      // Hide the loading wrapper
      document.getElementById('loading-wrapper').style.display = 'none';
      document.body.style.overflow = 'auto';

      // Scroll to bottom of chat
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