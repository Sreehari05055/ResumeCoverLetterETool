    const submitButton = document.getElementById('submit-btn');
    const chatForm = document.getElementById('chat-form')
    const chatBox = document.getElementById('chat-box');
    const inputField = document.getElementById('question');
    const fileInput = document.getElementById('file-upload');
    const openSettingsButton = document.getElementById('open-settings');
    const closeSettingsButton = document.getElementById('close-settings');
    const settingsPopup = document.getElementById('settings-popup');
    const overview = document.getElementById('Overview');

    function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
    }



    function typeText(element, sentences, delay = 50) {
        let sentenceIndex = 0; // Sentence index
        function typeNextSentence() {
            if (sentenceIndex < sentences.length) {
                element.innerHTML += sentences[sentenceIndex] + ' '; // Add sentence with a line break
                sentenceIndex++;
                scrollToBottom();
                setTimeout(typeNextSentence, delay); // delay before typing next sentence
            }
        }
        typeNextSentence();
    }




     chatForm.addEventListener('submit', function(event) {
     event.preventDefault(); // Prevent multiple submissions

     if(submitButton.disabled) {
        return;
     }
        submitButton.disabled = true;
        submitButton.style.opacity = "0.5";
        const userMessage = inputField.value.trim();

        const formData = new FormData();

        for (const file of fileInput.files)  {
        formData.append('uploaded_file', file);
        }
        if(userMessage || (fileInput.files.length > 0  && fileInput.files.length < 3))
        {
         if ((fileInput.files.length > 0 && fileInput.files.length < 3) && (userMessage)) {
            const sortFileName = Array.from(fileInput.files).map(file => file.name).join(', ');

            const userBubble = document.createElement('div');
            userBubble.classList.add('chat-bubble', 'user-bubble');
            userBubble.textContent =`Uploaded files: ${sortFileName}\n${userMessage}`
            chatBox.appendChild(userBubble);
            formData.append('user_input', `Uploaded files: ${sortFileName}\n${userMessage}`);
         }
         else if (userMessage){
            // Add user message to chat
            const userBubble = document.createElement('div');
            userBubble.classList.add('chat-bubble', 'user-bubble');
            userBubble.textContent = userMessage;
            chatBox.appendChild(userBubble);
            formData.append('user_input', userMessage);
         }
            inputField.value = '';
            fileInput.value = '';

            fetch(botResponseUrl, {
            method: 'POST',
            headers: {
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value, // CSRF token for Django
            },
              credentials: 'same-origin', // Include cookies for session management
              body: formData
            })
             .then(response => response.json())
            .then(data => {
             if (data.error) {
                const errorMessage = document.createElement('div');
                errorMessage.classList.add('chat-bubble', 'bot-bubble');
                errorMessage.textContent = data.error; // Display error message
                chatBox.appendChild(errorMessage);
             }
             else{
                const botBubble = document.createElement('div');
                botBubble.classList.add('chat-bubble', 'bot-bubble');
                chatBox.appendChild(botBubble);

                // Split response into sentences for progressive typing
                const sentences = data.bot_response.split('. ').map(sentence => sentence.trim()).filter(sentence => sentence);

                // Typing effect
                typeText(botBubble, sentences);

                scrollToBottom();
                }

        })
        .catch(error => {
                console.error('Error fetching bot response:', error);
            }).finally(() => {

            // Re-enable the submit button after the response is processed
            submitButton.style.opacity = "1";
            submitButton.disabled = false;

             });
        }
    });




        function toggleSubmitButton() {

        // Show the submit button only if there's input in the field
        if (inputField.value.trim() !== "") {
            submitButton.style.opacity = "1";
            submitButton.style.visibility = "visible";
            submitButton.disabled = false;
        } else {
            submitButton.style.opacity = "0";
            submitButton.style.visibility = "hidden";
            submitButton.disabled = true;
        }
    }




// Open modal when settings button is clicked
openSettingsButton.addEventListener('click', () => {
    settingsPopup.classList.add('is-active');
});

// Close modal when the close button is clicked
closeSettingsButton.addEventListener('click', () => {
    settingsPopup.classList.remove('is-active');
});

// Close the modal when clicking outside of it
settingsPopup.querySelector('.modal-background').addEventListener('click', () => {
    settingsPopup.classList.remove('is-active');
});



document.getElementById('clear-form').addEventListener('submit', function(event) {
    event.preventDefault();

    fetch(clearChatUrl, {
       method: 'POST',
       headers: {
       'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
       },
       credentials: 'same-origin'
    })
    .then(response => {
            if (response.ok) {
                const chatBubbles = document.querySelectorAll('.chat-bubble');
                chatBubbles.forEach(bubble => {
                bubble.remove();  // This will remove each chat bubble
                });
            }
       });
});
