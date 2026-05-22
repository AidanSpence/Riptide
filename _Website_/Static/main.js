



const playlist = [
{
    title: "No playlists loaded",
    duration: "N/a",
},     
];

const userIconPath = "assets/userIcon.svg"

const menuUpPath = "assets/arrowUp.svg"

const menuDownPath = "assets/arrowDown.svg"













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

async function fetchFlask() {
    try {
        const response = await fetch('http://localhost:5000/api/chat');
        const data = await response.json();

        console.log(data.chatbot_txt);
        return data.chatbot_txt
    } catch (error) {
        console.error('Error fetching data:', error);
    }
    
}   



async function loadPlaylists() {



    const response = playlist;

    // const response = await fetch("http://127.0.0.1:5000/Playlists");  // local flask testing (flask ip)      
    
    // const response = await fetch("999.999.99.99");  // AWS backend testing (add flask ip)

    const playlistContainer = document.getElementById("playlist-grid");

    let idloop = 0;

    playlist.forEach(playlist => {
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
        
        temphtml += '<img'

        box.innerHTML = temphtml

        playlistContainer.appendChild(box);
        dropdownCreate('box_' + idloop)
    });

}

async function loadchat(text, id){
    
    let chathtml = "";

    const chatItem = document.createElement("p");

    const chatContainer = document.getElementById("chatbox-window");

    chatItem.className = "chat-item";
    
    chathtml += `<p>${text}</p>`


    if (id == '0') { // left
        chatItem.style.textAlign = 'start'
        chatItem.style.marginRight = '5%'
    }
    if (id == '1') { // right
        chatItem.style.textAlign = 'end'
        chatItem.style.marginLeft = '5%'
    }
    chatItem.innerHTML = chathtml;

    chatContainer.appendChild(chatItem)
}









async function init() {
    loadPlaylists();
    iconCreate();
}
async function chatRefresh() {
    loadchat(await fetchFlask(), 0);
}
init();
chatRefresh()
chatRefresh()
chatRefresh()
