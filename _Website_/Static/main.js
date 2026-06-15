const playlist = []

const userIconPath = "assets/userIcon.svg";

const menuUpPath = "assets/arrowUp.svg";

const menuDownPath = "assets/arrowDown.svg";

const sendButtonPath = "assets/send.svg";

const BACKEND_ADDRESS = "0.0.0.0:5000/" // PRODUCTION ADDRESS, MAYBE I GET FROM ENV VAR LATER?

const username = document.getElementById("userName")



function sendButtonCreate() {
/* This creates both the button and also contains the listner for the button */
    const chatbox = document.getElementById("chatbot-input-button");

    const sendButton = document.createElement("img");

    sendButton.src = sendButtonPath;
    sendButton.alt = "Send Button";
    sendButton.classList.add("send-button");
    sendButton.id = "send-button";

    sendButton.addEventListener('click', () => { // listener
        flaskChatSendResponse()
    });

    chatbox.appendChild(sendButton);
}

function iconCreate(){
    const userIcon = document.createElement("img");
    userIcon.src = userIconPath;
    userIcon.alt = "User icon";
    userIcon.style.width = '100%'
    userIcon.style.height = '100%'
    document.getElementById("userIcon").appendChild(userIcon);
}

function dropdownCreate(ID){
    const dropdown = document.createElement("img");
    dropdown.src = menuDownPath;
    dropdown.alt = "Dropdown menu";
    dropdown.className = "dropdown-arrow"
    document.getElementById(ID).appendChild(dropdown);
}



function chatItemCreate(ID){ // ID == Chatbox ID
    const chatItem = document.createElement("p");
    chatItem.src = menuDownPath;
    chatItem.alt = "Text";
    document.getElementById(ID).appendChild(chatItem);
}






async function playlistFetchFlask() {
    try {
        const response = await fetch(`${BACKEND_ADDRESS}/api/playlist`);
        const data = await response.json();

        console.log("Playlist Flask");
        console.log(data);

        return data.playlist_data

    } catch (error) {
        console.error('Error fetching data:', error);
        return [
            { 
                title: "No playlists loaded",
                duration: "N/a",
            }
        ];
    }
}


// FLASK FETCH FUNCTIONS END





async function loadPlaylists() {

    const playlistContainer = document.getElementById("playlist-grid");

    playlistContainer.innerHTML = "";
    
    const playlists = await playlistFetchFlask();
    
    let idloop = 0;
    
    playlists.forEach(
        playlist => 
    {
        let temphtml = "";
        const box = document.createElement("div");

        idloop += 1;
        box.className = "playlist-item";
        box.id = 'box_' + idloop;

        if (playlist.title) {
            temphtml += `<h3>${playlist.title}</h3>`;
        }

        if (playlist.duration) {
            temphtml += `<p>Duration: ${playlist.duration}</p>`;
        }

        //temphtml += `<img src="default.jpg" alt="Playlist cover">`;

        box.innerHTML = temphtml;

        playlistContainer.appendChild(box);

        dropdownCreate('box_' + idloop);
    });
}

async function loadChat(text, id){
    /* This is for loading previous chats, it takes an input from flask */
    
    let chathtml = "";
    const chatItem = document.createElement("p");

    const chatContainer = document.getElementById("chatbox-window");



    try {
        chatItem.className = "chat-item";
        chathtml += `<p>${text}</p>`

        if (id == '0') { // left
            chatItem.style.alignSelf = 'start'
            chatItem.style.marginRight = '5%'
        }
        if (id == '1') { // right
            chatItem.style.alignSelf = 'end'
            chatItem.style.marginLeft = '5%'
        }
        chatItem.innerHTML = chathtml;

        chatContainer.appendChild(chatItem)
    }
    catch (error) {
        console.error('Error fetching data:', error);}
}


async function getChatBoxText() {
    let box_text = document.getElementById("chatboxinput").value
    console.log(box_text)
    return box_text
}



async function flaskChatSendResponse() {
    const tosend = await getChatBoxText();
    if (tosend != "")
    {
        loadChat(tosend, 1)
        document.getElementById('chatboxinput').value = ""
        console.log(`Sent: `,tosend);

        try {
            const response = await fetch(`${BACKEND_ADDRESS}api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_txt: tosend
                })
            });

            const data = await response.json();
            console.log(`recieved: ${data}`)
            console.log(data);
            if (data)
                console.log(data.msg_id)
                console.log(data.chatbot_txt)
                loadChat(data.chatbot_txt, data.msg_id)

        } catch (error) {
            console.error("Error sending message:", error);
        }
    }
}


async function init() {
    iconCreate();
    sendButtonCreate();
    textAreaHandler()
    username.textContent = "George"
}

// refreshes the playlists, in a function for when additional functionality required
async function playlistRefresh() {
    loadPlaylists()
}




async function infoPopup() {
    
}

function textAreaHandler() {

    document.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                flaskChatSendResponse();
                document.getElementById('chatboxinput').value = ""
            }
        });
}


async function navButtonsListen() {

    const playlistButton = document.getElementById("playlistsButton");
    const infoButton = document.getElementById("infoButton");
    const loginButton = document.getElementById("loginButton");
    const chatButton = document.getElementById("chatButton");
    playlistButton.addEventListener('click', () => { // listener
        console.log("playlist button clicked")
    });
    infoButton.addEventListener('click', () => { // listener
        console.log("info button clicked")
    });
    loginButton.addEventListener('click', () => { // listener
        console.log("login button clicked")
    });
        chatButton.addEventListener('click', () => { // listener
        console.log("Chats button clicked")
    });
}

async function navButtonsCloseListen() {
    const infoPopupClose = document.getElementById("infoPopupClose")
    infoPopupClose.addEventListener('click', () => { // listener
        console.log("close button clicked")
    });
}

init();
playlistRefresh()
navButtonsListen()