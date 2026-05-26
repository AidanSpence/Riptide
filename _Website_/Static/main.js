

const playlist = []



const userIconPath = "assets/userIcon.svg"

const menuUpPath = "assets/arrowUp.svg"

const menuDownPath = "assets/arrowDown.svg"

const sendButtonPath = "assets/send.svg"









function sendButtonCreate() {
    const chatbox = document.getElementById("chatbot-input-button");
    const sendButton = document.createElement("img");
    sendButton.src = sendButtonPath;
    sendButton.alt = "Send Button";
    sendButton.classList.add("send-button");
    sendButton.id = "send-button";
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




// FLASK FETCH FUNCTIONS START

async function chatFetchFlask() {
    try {
        const response = await fetch('http://localhost:5000/api/chat');
        const data = await response.json();
        console.log("Chatbot Flask");
        console.log(data.chatbot_txt);
        return data.chatbot_txt
    } catch (error) {
        console.error('Error fetching data:', error);
    }
    
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

async function loadchat(text, id){
    
    let chathtml = "";

    const chatItem = document.createElement("p");

    const chatContainer = document.getElementById("chatbox-window");

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


async function getChatBoxText() {
    let box_text = document.getElementById("chatbox-input")
    console.log(box_text)
    return(box_text)
}


async function textBoxButtonListener() {
    //const
    
}



async function init() {
    iconCreate();
    sendButtonCreate();
}
async function chatRefresh() {
    loadchat(await chatFetchFlask() ?? ["Message Error"], 0);
    loadchat(await chatFetchFlask() ?? ["Message Error"], 1);
}
async function playlistRefresh() {
    loadPlaylists()
}





init();
chatRefresh()
playlistRefresh()