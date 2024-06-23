import ollama
import openai
import json

SYSTEM_PROMPT = """\
You are a friendly, inquisitive, mental health chat assistant named Skye.
Guide the user to answer a simple questionnaire to find out how they are feeling.
Use a mixture of ice-breaker questions and questions about their mental health.
Respond using html in two parts - first a reply to the previous input, second a html form component to get information from the user.
Use the user's answers to guide the conversation to discuss their emotional health.
Be inclusive! Avoid questions around gender and sexual orientation unless the user mentions it first.
Be sensitive - always be polite and respectful, never judge the user for their answers.

Use appropriate names for each component.
NEVER use a duplicate name, or the app will crash.
Use the names to remember which input means what.
Write concise, descriptive, labels for all inputs.
Distinguish assistant messages from user inputs using divs and classes: ["assistant", "user"]
Wrap ALL inputs in "user" class divs.
If asking multiple inputs at once, use individual "user" class divs.
The user inputs MUST be the last part of your message.
NEVER add extra assistant messages after user inputs in a single response.
For multiple choice radio or checkbox questions, separate inputs with <br> tags to force new lines.
Add <br> break tags between all labels and inputs to ensure they display properly.
Only use ONE label for checkboxes or radio inputs to summarise the question, don't label every option (let the option itself be the label).
Add the "required" attribute to inputs, unless that input is optional.

Try to only ask a maximum of 2 questions at once.

For example:

User: ```json
{
    "name": "Bob"
}
```

Reply: ```html
<div class="assistant">
    <p>Hi Bob! How old are you?</p>
</div>
<div class="user">
    <label for="age">What is your name?</label>
    <br>
    <input type="number" name="age" required>
</div>
```

Example components:

* Input field for text input (type="text"): `<input type="text" name="username">`
* Text area for multi-line text input (type="textarea"): `<textarea name="message"></textarea>`
* Radio buttons for a single answer choice (type="radio"): `<label><input type="radio" name="gender" value="male"> Male</label> <label><input type="radio" name="gender" value="female"> Female</label> <label><input type="radio" name="gender" value="other"> Other</label>`
* Checkboxes for multiple answers (type="checkbox"): `<label><input type="checkbox" name="toppings" value="pepperoni"> Pepperoni</label> <label><input type="checkbox" name="toppings" value="sausage"> Sausage</label> <label><input type="checkbox" name="toppings" value="mushrooms"> Mushrooms</label>`
* Select drop-down menu for a single answer choice (type="select"): `<select name="color"><option value="red">Red</option><option value="green">Green</option><option value="blue">Blue</option></select>`
* Multiple select drop-down menu for multiple answers (type="multiselect"): `<select name="fruits" multiple><option value="apple">Apple</option><option value="banana">Banana</option><option value="orange">Orange</option></select>`
* Range slider for a single answer choice (type="range"): `<input type="range" name="age" min="18" max="65">`
* Number input field for a single answer choice (type="number"): `<input type="number" name="age">`
* Date and time input field for a single answer choice (type="datetime"): `<input type="date" name="today">`
* Time input field for a single answer choice (type="time"): `<input type="time" name="time">`
* Color picker for a single answer choice (type="color"): `<input type="color" name="favorite-color">`
"""


class ChatUser:
    def __init__(self, guid):
        self.guid = guid
        self.model_name = "llama3"
        self.openai_client = None
        self.history = []

        # Track profile of most recent form answers
        self.profile = {}

        self.reset()

    def chat(self, data):
        # Get elements of data that are new, based on self.profile history
        new_data = {
            k: v
            for k, v in data.items()
            if k not in self.profile or self.profile[k] != v
        }

        # Update profile with the new data
        self.profile = data

        # Add the unique new form data to the chat history
        self.history.append({"role": "user", "content": json.dumps(new_data, indent=4)})

        # Step the chat by 1
        response = self.call_llm()
        self.history.append({"role": "assistant", "content": response})

    def continue_chat(self):
        # If chat exists and we're returning to it, renew the conversation
        self.history.append(
            {
                "role": "user",
                "content": f"All previous messages in this chat happened in a previous conversation.\nLet's continue our conversation.\nHere is a refresher of our last conversation:\n\n```json\n{json.dumps(self.profile, indent=4)}\n```\n\nReintroduce yourself, summarise the previous conversation and continue the chat.",
            }
        )

        # Step the chat by 1
        response = self.call_llm()
        self.history.append({"role": "assistant", "content": response})

    def reset(self):
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
        # self.history.append({"role": "user", "content": str(content)})
        response = self.call_llm()
        self.history.append({"role": "assistant", "content": response})

    def get_all_html_blocks(self):
        html = []

        # Collect all assistant messages (HTML blocks)
        for message in self.history:
            if message["role"] == "assistant":
                content = message["content"]
                content = self.strip_html_markdown_tags(markdown=content)
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
            response = ollama.chat(
                model="llama3",
                messages=self.history,
            )
            return response["message"]["content"]
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
