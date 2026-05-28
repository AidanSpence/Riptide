const playlist = []

const userIconPath = "assets/userIcon.svg";

const menuUpPath = "assets/arrowUp.svg";

const menuDownPath = "assets/arrowDown.svg";

const sendButtonPath = "assets/send.svg";

const buttonlisten = document.getElementById("send-button");






function sendButtonCreate() {
/* This creates both the button and also contains the listner for the button */
    const chatbox = document.getElementById("chatbot-input-button");

    const sendButton = document.createElement("img");

    sendButton.src = sendButtonPath;
    sendButton.alt = "Send Button";
    sendButton.classList.add("send-button");
    sendButton.id = "send-button";

    sendButton.addEventListener('click', () => { // listener
        // This needs to be changed to chatSendFlask
        loadChatFlask()
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
    dropdown.className = "dropdownArrow"
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
        const response = await fetch('http://localhost:5000/api/playlist');
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

async function loadchat(){
    
    let chathtml = "";
    let id = 0;
    let text = "ERROR"

    const chatItem = document.createElement("p");

    const chatContainer = document.getElementById("chatbox-window");

    try {
        const response = await fetch('http://localhost:5000/api/chat');
        const data = await response.json();
        console.log("Chatbot Flask");
        console.log(data.chatbot_txt);
        console.log(data.msg_id);
        let text = data.chatbot_txt;
        id = data.msg_id;
        chatItem.className = "chat-item";
        chathtml += `<p>${text}</p>`
    } 
    catch (error) {
        console.error('Error fetching data:', error);
    }
    








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


async function getChatBoxText() {
    let box_text = document.getElementById("chatbox-input")
    console.log(box_text)
    return(box_text)
}




async function init() {
    iconCreate();
    sendButtonCreate();
}

// refreshes the playlists, in a function for when additional functionality required
async function playlistRefresh() {
    loadPlaylists()
}

// Simplifies the line into a smaller function
async function loadChatFlask() {
    loadchat()
} 




init();
playlistRefresh()