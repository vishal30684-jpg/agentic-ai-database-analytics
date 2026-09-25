
const API_URL = "http://127.0.0.1:8000";



// DOM ELEMENTS


const questionInput = document.getElementById("questionInput");
const askButton = document.getElementById("askButton");
const chatBox = document.getElementById("chatBox");

const newChatButton = document.getElementById("newChatButton");
const conversationList = document.getElementById("conversationList");

const chatTitle = document.getElementById("chatTitle");



// CURRENT CONVERSATION


let currentConversationId = null;



// LOAD CONVERSATIONS


async function loadConversations() {

    try {

        const response = await fetch(
            `${API_URL}/conversations`
        );

        if (!response.ok) {
            throw new Error("Failed to load conversations");
        }

        const data = await response.json();

        conversationList.innerHTML = "";


        if (data.conversations.length === 0) {

            conversationList.innerHTML = `
                <div style="color:#aaa; padding:10px;">
                    No chats yet
                </div>
            `;

            return;
        }


    
        data.conversations.forEach(conversation => {

            const item = document.createElement("div");

            item.className = "conversation-item";

            if (conversation.id === currentConversationId) {
                item.classList.add("active");
           }

           const title = document.createElement("span");

            title.textContent = conversation.title;

            title.addEventListener(
              "click",
              () => {
                loadConversation(
                   conversation.id,
                   conversation.title
                );
              }
        
        );

    const deleteButton = document.createElement("button");

    deleteButton.textContent = "🗑️";

    deleteButton.className = "delete-chat-button";

    deleteButton.addEventListener(
        "click",
        (event) => {
            event.stopPropagation();

            deleteConversation(
                conversation.id
            );
        }
    );

    item.appendChild(title);
    item.appendChild(deleteButton);

    conversationList.appendChild(item);
   });



    } catch (error) {

        console.error(
            "Error loading conversations:",
            error
        );

    }
}


// LOAD ONE CONVERSATION


async function loadConversation(
    conversationId,
    title
) {

    try {

        currentConversationId = conversationId;

        chatTitle.textContent = title;


        const response = await fetch(
            `${API_URL}/conversations/${conversationId}/messages`
        );


        if (!response.ok) {
            throw new Error(
                "Failed to load conversation"
            );
        }


        const data = await response.json();


        chatBox.innerHTML = "";


        if (data.messages.length === 0) {

            chatBox.innerHTML = `
                <div class="message ai-message">
                    <strong>AI:</strong>
                    This is a new conversation. 👋
                </div>
            `;

        }


        data.messages.forEach(message => {

            if (message.role === "user") {

                addUserMessage(
                    message.content
                );

            } else {

                addAIMessage(
                    message.content
                );

            }

        });


        await loadConversations();


        scrollToBottom();

        questionInput.focus();


    } catch (error) {

        console.error(error);

        chatBox.innerHTML = `
            <div class="message ai-message">
                <strong>AI:</strong>
                Unable to load this conversation.
            </div>
        `;

    }
}


// Delete conversation
async function deleteConversation(conversationId) {

    const confirmed = confirm(
        "Are you sure you want to delete this chat?"
    );

    if (!confirmed) {
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/conversations/${conversationId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error(
                "Failed to delete conversation"
            );
        }

        // If deleting the currently open chat
        if (currentConversationId === conversationId) {
            currentConversationId = null;

            chatTitle.textContent =
                "AI Database Assistant";

            chatBox.innerHTML = `
                <div class="message ai-message">
                    <strong>AI:</strong>
                    Chat deleted. 👋
                    <br>
                    Start a new conversation.
                </div>
            `;
        }

        await loadConversations();

        questionInput.focus();

    } catch (error) {

        console.error(error);

        alert(
            "Unable to delete this chat."
        );
    }
}


// CREATE NEW CHAT


async function createNewChat() {

    try {

        const response = await fetch(
            `${API_URL}/conversations`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    title: "New Chat"
                })
            }
        );


        if (!response.ok) {
            throw new Error(
                "Failed to create conversation"
            );
        }


        const data = await response.json();


        currentConversationId =
            data.conversation_id;


        chatTitle.textContent = "New Chat";


        chatBox.innerHTML = `
            <div class="message ai-message">
                <strong>AI:</strong>
                Hello! 👋
                <br>
                Ask me anything about your database.
            </div>
        `;


        await loadConversations();


        scrollToBottom();

        questionInput.focus();


    } catch (error) {

        console.error(error);

        alert(
            "Unable to create a new chat."
        );

    }
}


// ASK QUESTION


async function askQuestion() {

    const question =
        questionInput.value.trim();


    if (!question) {
        return;
    }


    // Show user message
   

    addUserMessage(question);


    questionInput.value = "";


  
    // Disable button
 

    askButton.disabled = true;

    askButton.textContent =
        "Thinking...";


    // Loading message
   

    const loadingMessage =
        document.createElement("div");


    loadingMessage.className =
        "message ai-message";


    loadingMessage.innerHTML =
        "<strong>AI:</strong> Thinking...";


    chatBox.appendChild(
        loadingMessage
    );


    scrollToBottom();


    try {

        const response = await fetch(
            `${API_URL}/ask`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    question: question,

                    conversation_id:
                        currentConversationId

                })

            }
        );


        if (!response.ok) {

            throw new Error(
                "Server error"
            );

        }


        const data =
            await response.json();


       
        // Remove loading
       

        loadingMessage.remove();


      
        // Save conversation ID
        

        currentConversationId =
            data.conversation_id;


        // Show AI response
        

        addAIMessage(
            data.answer
        );


        
        // Refresh sidebar
        

        await loadConversations();


    } catch (error) {

        console.error(error);


        loadingMessage.remove();


        addAIMessage(
            "Unable to connect to the server."
        );

    }


    // Enable button
   

    askButton.disabled = false;

    askButton.textContent = "Ask";


    scrollToBottom();

    questionInput.focus();

}



// ADD USER MESSAGE


function addUserMessage(message) {

    const div =
        document.createElement("div");


    div.className =
        "message user-message";


    div.innerHTML = `
        <strong>You:</strong>
        ${escapeHtml(message)}
    `;


    chatBox.appendChild(div);

}


// ADD AI MESSAGE


function addAIMessage(message) {

    const div =
        document.createElement("div");


    div.className =
        "message ai-message";


    div.innerHTML = `
        <strong>AI:</strong>
        ${marked.parse(message)}
    `;


    chatBox.appendChild(div);

}


// ESCAPE HTML


function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}



// SCROLL


function scrollToBottom() {

    chatBox.scrollTop =
        chatBox.scrollHeight;

}



// EVENT LISTENERS


askButton.addEventListener(
    "click",
    askQuestion
);


newChatButton.addEventListener(
    "click",
    createNewChat
);


questionInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            askQuestion();

        }

    }
);



// INITIAL LOAD


async function initialize() {

    await loadConversations();


    chatBox.innerHTML = `
        <div class="message ai-message">
            <strong>AI:</strong>
            Hello! 👋
            <br>
            Select a chat from the sidebar
            or click <strong>+ New Chat</strong>.
        </div>
    `;


    questionInput.focus();

}


initialize();

async function checkServerStatus() {
    const statusElement = document.getElementById("serverStatus");

    try {
        const response = await fetch(`${API_URL}/health`);

        if (response.ok) {
            statusElement.textContent = "● Online";
            statusElement.classList.remove("offline");
            statusElement.classList.add("online");
        } else {
            throw new Error("Server unavailable");
        }

    } catch (error) {
        statusElement.textContent = "● Offline";
        statusElement.classList.remove("online");
        statusElement.classList.add("offline");
    }
}

checkServerStatus();
setInterval(checkServerStatus, 10000);