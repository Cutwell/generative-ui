const tour = new Shepherd.Tour({
    useModalOverlay: true,
    defaultStepOptions: {
        classes: 'shadow-md bg-purple-dark',
        exitOnEsc: true,
        cancelIcon: {
            enabled: true
        },
        scrollTo: { behavior: 'smooth', block: 'center' }
    }
});

document.addEventListener('DOMContentLoaded', function () {
    tour.addStep({
        id: 'step-00',
        text: 'Welcome to the <code>Untitled Goose Chatbot</code>! This is a fully-functional UI demo for chat-based generative AI web-apps - let me show you around!',
        buttons: [
            {
                text: 'Next (1/5)',
                action: tour.next
            }
        ]
    });

    tour.addStep({
        id: 'step-01',
        text: 'This is the chat input - type your messages here and hit <kbd>Enter</kbd> or click the submit button to send a message. Use <kbd>Shift</kbd>+<kbd>Enter</kbd> to insert normal new lines.',
        attachTo: {
            element: '#mainForm',
            on: 'top'
        },
        buttons: [
            {
                text: 'Next (2/5)',
                action: tour.next
            }
        ]
    });

    tour.addStep({
        id: 'step-02',
        text: 'Use this menu to return to the home page (this preserves chat history), or reset the chat (this deletes all chat history). If you don\'t reset your chat, you can return to it any time using the back button on your browser.',
        attachTo: {
            element: '.button-menu-container',
            on: 'top'
        },
        buttons: [
            {
                text: 'Next (3/5)',
                action: tour.next
            }
        ]
    });

    tour.addStep({
        id: 'step-03',
        text: 'Click here to open the LLM Settings pop-up window - choose between Llama 3 and OpenAI GPT 3.5 (switch LLM anytime, even mid-session) (OpenAI reqiures API token, tokens are saved per chat session).',
        attachTo: {
            element: '#open-popup-3',
            on: 'top'
        },
        buttons: [
            {
                text: 'Next (4/5)',
                action: tour.next
            }
        ]
    });

    tour.addStep({
        id: 'step-04',
        text: 'That\'s it! This chatbot is pretending to be a Goose, but you can customise the underlying LLM however you want. Full response streaming is also supported, enabling fast and dynamic responses!',
        buttons: [
            {
                text: 'Finish (5/5)',
                action: tour.next
            }
        ]
    });

    // Only start tour if user has not seen tour before
    if (localStorage.getItem("seen_tour") == null) {
        tour.start();
        localStorage.setItem("seen_tour", "true");
    }
})