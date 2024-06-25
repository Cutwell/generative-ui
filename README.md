# Generative UI 🏗️💬
Help your LLM apps escape the chat box!

## Features

* Generative UI concept - let your LLM chatbots interact with users in new interesting ways.
* Private, local, execution with Ollama - optimised for Llama3.

## Demos

### Skye: A friendly emotional-health chatbot

* Proof of concept generative UI use-case.
* Iteratively constructs a HTML form UI during conversation.
* Preserves chat history in-between browser sessions, resummarises previous conversation upon continuance.

#### Try yourself!

```zsh
poetry install
poetry run uvicorn demos.skye.src.main:app
```

### Goose: "Honk"

* Standardised chatbot UI.
* Supports real-time streaming responses from LLM to UI.
* Preserves chat history in-between browser session, restores history in full on continuance.

#### Try yourself!

```zsh
poetry install
poetry run uvicorn demos.goose.src.main:app
```

## License
MIT
