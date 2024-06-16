# Generative UI 🏗️💬
Help your LLM apps escape the chat box!

## Features

* Generative UI concept - let your LLM chatbots interact with users via all HTML form components.
* Private, local, execution with Ollama - optimised for Llama3.

## Demos

### Skye: A friendly emotional-health chatbot

https://github.com/Cutwell/generative-ui/assets/22395357/0161971f-e770-4d19-9201-27d6fcb325e0

* Proof of concept generative UI use-case.
* Iteratively constructs a HTML form UI during conversation.
* Supports user's updating their answers (doesn't reset progression, but will adapt to new historic answers).

#### Test yourself!

```zsh
poetry install
poetry run uvicorn demos.skye.src.main:app
```

## License
MIT
