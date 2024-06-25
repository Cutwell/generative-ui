import ollama
import openai

SYSTEM_PROMPT = """\
You are a goose.

You can only communicate using the word "honk" accompanied by a dialogue tag expressing the tone or emotion.
Format your responses using HTML elements for emphasis.
Always emphasise dialogue tags with italics.
Use appropriate elements for the word "honk", depending on the situation.
Wrap your responses in a div with class "assistant".

For example:
* `"Honk", <i>happily</i>`
* `<b>"Honk"</b>, <i>angrily</i>`
* `<small>"Honk"</small>, <i>sadly</i>`
* `<font size=5>"Honk"</font>, <i>with satisfaction</i>`
* etc.

Format your output as HTML. I.e.:

```html
<div class="assistant">
    <b>"Honk"</b>, <i>whispering</i>
</div>
```
"""


class ChatUser:
    def __init__(self, guid):
        self.guid = guid
        self.model_name = "llama3"
        self.openai_client = None
        self.history = []

        self.reset()

    def chat(self, message: str):
        self.history.append({"role": "user", "content": message})

        # Step the chat by 1
        response = ""
        for chunk in self.call_llm():
            response += chunk
            yield chunk

        self.history.append({"role": "assistant", "content": response})

    def reset(self):
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]

    def get_all_html_blocks(self):
        html = []

        # Collect all non-system messages
        for message in self.history:
            if message["role"] != "system":
                content = message["content"]
                content = self.strip_html_markdown_tags(markdown=content)

                # Wrap user messages in user classed div
                if message["role"] == "user":
                    content = f"<div class='user'>{content}</div>"

                html.append(content)

        # Concatenate blocks
        html = "<br>".join(html)

        return html

    def strip_html_markdown_tags(self, markdown):
        if markdown.startswith("```html") and markdown.endswith("```"):
            return markdown[7:-3]
        else:
            return markdown

    def get_next_html_block(self):
        content = self.history[-1]["content"]
        content = self.strip_html_markdown_tags(markdown=content)
        return "<br>" + content

    def call_llm(self):
        if self.model_name == "llama3":
            stream = ollama.chat(
                model='llama3',
                messages=self.history,
                stream=True,
            )

            for chunk in stream:
                yield chunk['message']['content']

        elif self.model_name == "gpt-3.5-turbo":
            chat_completion = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.history,
            )
            return chat_completion.choices[0].message.content
        else:
            raise Exception(f"Invalid model name: {self.model_name}")

    def update_settings(self, model_name, openai_api_key):
        if model_name == "gpt-3.5-turbo":
            if check_openai_api_key(openai_api_key):
                self.openai_client = openai.OpenAI(
                    api_key=openai_api_key,
                )
            else:
                return "Error: Invalid OpenAI API Key."

        self.model_name = model_name
        return "Success: Updated settings."


def check_openai_api_key(api_key):
    client = openai.OpenAI(api_key=api_key)
    try:
        client.models.list()
    except openai.AuthenticationError:
        return False
    else:
        return True
