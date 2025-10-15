document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatbotMessages = document.getElementById('chatbotMessages');
    const errorMessage = document.getElementById('errorMessage');

    const BACKEND_URL = 'https://product-form-altibbe.onrender.com//generate-question';
'; 

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    async function sendMessage() {
        const userText = userInput.value.trim();
        if (userText === '') return;

        appendMessage('user', userText);
        userInput.value = ''; // Clear input

        errorMessage.style.display = 'none'; // Hide any previous errors
        appendLoadingMessage(); // Show loading indicator

        try {
            const response = await fetch(BACKEND_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ product_description: userText }),
            });

            removeLoadingMessage(); // Hide loading indicator

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to generate questions.');
            }

            const data = await response.json();
            // --- CHANGE HERE ---
            displayGeneratedQuestionAsChatMessage(data); // Call the new function
            // --- END CHANGE ---

        } catch (error) {
            console.error('Error:', error);
            removeLoadingMessage(); // Hide loading indicator even on error
            errorMessage.textContent = `Error: ${error.message}`;
            errorMessage.style.display = 'block';
            appendMessage('bot', `Oops! Something went wrong: ${error.message}. Please try again.`);
        }
    }

    function appendMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.innerHTML = `<p>${text}</p>`;
        chatbotMessages.appendChild(messageDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Scroll to bottom
    }

    function appendLoadingMessage() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot-message loading-message';
        loadingDiv.id = 'loadingBotMessage';
        loadingDiv.innerHTML = '<p>Generating questions...</p>';
        chatbotMessages.appendChild(loadingDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    function removeLoadingMessage() {
        const loadingDiv = document.getElementById('loadingBotMessage');
        if (loadingDiv) {
            loadingDiv.remove();
        }
    }

   
    function displayGeneratedQuestionAsChatMessage(data) {
        if (!data || !data.question || !data.question.text) {
            appendMessage('bot', "I couldn't generate a question. Could you describe it in more detail?");
            return;
        }

        const questionText = data.question.text;
        appendMessage('bot', questionText); // Simply append the question as a bot message
    }
  
});