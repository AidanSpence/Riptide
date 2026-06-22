// Global Confguration
const BACKEND_ADDRESS = window.location.origin;
//const BACKEND_ADDRESS = 'http://127.0.0.1:5000'
const playlist = [];

const paths = {
  userIcon: "assets/userIcon.svg",
  menuUp: "assets/arrowUp.svg",
  menuDown: "assets/arrowDown.svg",
  sendButton: "assets/send.svg",
  fallbackImage: "assets/fallback-image.png"
};

// Spotify Elements
const CLIENT_ID = '3eed8ec7a7a8454393d3e118574bdd05'; 
const REDIRECT_URI = 'https://d11r265tlaxh0o.cloudfront.net/';
//const REDIRECT_URI = 'http://127.0.0.1:5500/_Website_/main.html';
const AUTH_ENDPOINT = 'https://accounts.spotify.com/authorize';
const RESPONSE_TYPE = 'code';
let SPOTIFY_TOKEN = null;

// Permissions requested
const SCOPES = [
    'user-read-private',
    'user-read-email',
    'playlist-read-private'
];

const authUrl = `${AUTH_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&scope=${encodeURIComponent(SCOPES.join(' '))}&response_type=${RESPONSE_TYPE}&show_dialog=true`;

const username = document.getElementById("userName");

// ==========================================
// Spotify Components
// ==========================================

function getAuthCode() {
    const params = new URLSearchParams(window.location.search);
    return params.get('code');
}

async function exchangeCodeForToken(code) {
    const res = await fetch(`${BACKEND_ADDRESS}/api/spotify-token?code=${code}`);
    const data = await res.json();
    console.log("Token exchange response:", data); // Check for errors here
    return data.access_token;
}

async function getPlaylists(token) {
    const response = await fetch(`https://api.spotify.com/v1/me/playlists`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (!response.ok) {
        console.error("Spotify API error:", await response.text());
        return [];
    }

    const data = await response.json();
    return data.items || [];
}

async function displayPlaylists(token) {
  if (!token) {
    console.log("No access token found in URL hash.");
    return;
  }

  const playlists = await getPlaylists(token);

  const playlistContainer = document.getElementById("playlistGrid");
  if (!playlistContainer) {
    console.log("playlistGrid not found");
    return;
  }

  playlistContainer.innerHTML = ""; // Clear
  console.log("Playlists received:", playlists);

  playlists.forEach((playlist, index) => {
    if (!playlist || !playlist.items) return; // Skip malformed items
    const boxId = `box_${index + 1}`;
    const playlistCard = document.createElement("div");

    playlistCard.className = "playlist-item";
    playlistCard.id = boxId;

    const imageUrl = playlist.images?.[0]?.url || paths.fallbackImage;

    playlistCard.innerHTML = `
      <img src="${imageUrl}" alt="${playlist.name} cover" width="150">
      <h3>${playlist.name}</h3>
      <p>${playlist.items.total} tracks</p>`;

    playlistContainer.appendChild(playlistCard);
    dropdownCreate(boxId);
  });
}

async function handleSpotifyLogin() {
    const code = getAuthCode();
    if (!code) return;

    const token = await exchangeCodeForToken(code);

    if (token) {
      SPOTIFY_TOKEN = token;
      displayPlaylists(token);
    }
}

// For adding playlist dropdowns
// async function getPlaylistTracks(playlistId, token) {
//     const response = await fetch(`https://spotify.com{playlistId}/tracks?limit=50`, {
//         method: 'GET',
//         headers: {
//             'Authorization': `Bearer ${token}`
//         }
//     });

//     const data = await response.json();
//     return data.items; // Array of track objects
//}

//   const playlistId = 'PlaylistId';

// ==========================================
// UI Components
// ==========================================

function sendButtonCreate() {
  const chatbox = document.getElementById("chatbotInputButton");
  if (!chatbox) {
    console.log("chatbotInputButton not found");
    return;
  }

  const sendButton = document.createElement("img");
  sendButton.src = paths.sendButton;
  sendButton.alt = "Send Button";
  sendButton.classList.add("send-button");
  sendButton.id = "send-button";

  sendButton.addEventListener("click", () => {
    // listener
    flaskChatSendResponse();
  });

  chatbox.appendChild(sendButton);
}

function iconCreate() {
  const iconContainer = document.getElementById("userIcon");
  if (!iconContainer) {
    console.log("userIcon not found");
    return;
  }

  const userIcon = document.createElement("img");
  userIcon.src = paths.userIcon;
  userIcon.alt = "User icon";
  userIcon.style.width = "100%";
  userIcon.style.height = "100%";

  iconContainer.appendChild(userIcon);
}

function dropdownCreate(targetId) {
  const parentContainer = document.getElementById(targetId);
  if (!parentContainer) {
    console.log(`${targetId}! not found`);
    return;
  }

  const dropdown = document.createElement("img");
  dropdown.src = paths.menuDown;
  dropdown.alt = "Dropdown menu";
  dropdown.className = "dropdown-arrow";

  parentContainer.appendChild(dropdown);
}

function chatItemCreate(targetId) {
  const chatContainer = document.getElementById(targetId);
  if (!chatContainer) {
    console.log(`${targetId}! not found`);
    return;
  }

  const chatItem = document.createElement("p");
  chatItem.textContent = "Text";

  chatContainer.appendChild(chatItem);
}

// ==========================================
// Data Fetch & Sync
// ==========================================

async function playlistFetchFlask() {
  try {
    const response = await fetch(`${BACKEND_ADDRESS}/api/playlist`);
    if (!response.ok)
      throw new Error(`HTTP network error: status ${response.status}`);

    const data = await response.json();
    return data.playlist_data;
  } catch (error) {
    console.error("Error fetching data:", error);
    return [
      {
        title: "No playlists loaded",
        duration: "N/a",
      },
    ];
  }
}

// async function loadPlaylists() {
//   const playlistContainer = document.getElementById("playlistGrid");
//   if (!playlistContainer) {
//     console.log("playlistGrid not found");
//     return;
//   }

//   playlistContainer.innerHTML = "";
//   const playlists = await playlistFetchFlask();

//   playlists.forEach((playlist, index) => {
//     const boxId = `box_${index + 1}`;
//     const cardBox = document.createElement("div");
//     cardBox.className = "playlist-item";
//     cardBox.id = boxId;

//     let contentStructure = "";
//     if (playlist.title) {
//       contentStructure += `<h3>${playlist.title}</h3>`;
//     }
//     if (playlist.duration) {
//       contentStructure += `<p>Duration: ${playlist.duration}</p>`;
//     }

//     cardBox.innerHTML = contentStructure;
//     playlistContainer.appendChild(cardBox);
//     dropdownCreate(boxId);
//   });
// }

// ==========================================
// Dialogue & Interface
// ==========================================

async function loadChat(text, alignmentId) {
  // This is for loading previous chats, it takes an input from flask
  const chatContainer = document.getElementById("chatboxWindow");
  if (!chatContainer) {
    console.log("chatboxWindow not found");
    return;
  }

  const chatItem = document.createElement("p");
  chatItem.className = "chat-item";
  chatItem.innerHTML = text;

  // Format element alignments based on id
  if (String(alignmentId) === "0") {
    // left
    chatItem.style.alignSelf = "start";
    chatItem.style.marginRight = "5%";
  }
  if (String(alignmentId) === "1") {
    // right
    chatItem.style.alignSelf = "end";
    chatItem.style.marginLeft = "5%";
  }

  chatContainer.appendChild(chatItem);
  chatContainer.scrollTop = chatContainer.scrollHeight; // Auto-scroll window
}

async function getChatBoxText() {
  const chatInput = document.getElementById("chatboxInput");
  if (!chatInput) {
    console.log("chatboxInput not found");
    return;
  }
  let box_text = chatInput.value;
  console.log(box_text);
  return box_text;
}

async function flaskChatSendResponse() {
  const tosend = await getChatBoxText();
  if (tosend != "") {

    loadChat(tosend, 1);

    document.getElementById('chatboxInput').value = ""

    console.log(`Sent: `, tosend);

    try {
      const response = await fetch(`${BACKEND_ADDRESS}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_txt: tosend }),
      });

      const data = await response.json();
      console.log(`recieved: ${data}`);

      if (data) {
        console.log(data.msg_id);
        console.log(data.chatbot_txt);
        loadChat(data.chatbot_txt, data.msg_id);
      }
    } catch (error) {
      console.error("Error sending message:", error);
    }
  }
}

// ==========================================
// Listeners
// ==========================================

async function navButtonsListen() {
  const playlistButton = document.getElementById("playlistsButton");
  const infoButton = document.getElementById("infoButton");
  const loginButton = document.getElementById("loginButton");
  const chatButton = document.getElementById("chatButton");

  // Placeholder button listerners
  if (playlistButton)
    playlistButton.addEventListener("click", () => {
        console.log("playlist button clicked");
        if (SPOTIFY_TOKEN) {
            displayPlaylists(SPOTIFY_TOKEN);
        } else {
            console.log("No Spotify token available — user may not be logged in");
        }
    });
  if (infoButton)
    infoButton.addEventListener("click", () => {
      console.log("info button clicked");
    });
  if (loginButton)
    loginButton.addEventListener("click", () => {
      console.log("login button clicked");
      window.location.href = authUrl;
    });
  if (chatButton)
    chatButton.addEventListener("click", () => {
      console.log("Chats button clicked");
    });
}

async function navButtonsCloseListen() {
  const infoPopupClose = document.getElementById("infoPopupClose");
  if (infoPopupClose) {
    infoPopupClose.addEventListener("click", () => {
      // listener
      console.log("close button clicked");
    });
  }
}

async function init() {
  iconCreate();
  sendButtonCreate();
  textAreaHandler();
  handleSpotifyLogin();
  if (username) username.textContent = "George";
}

// refreshes the playlists, in a function for when additional functionality required
async function playlistRefresh() {
  if (SPOTIFY_TOKEN) {
    displayPlaylists(SPOTIFY_TOKEN);
  } else {
    console.log("No Spotify token available — user may not be logged in");
  }
  //loadPlaylists();
}

function textAreaHandler() {

    document.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                flaskChatSendResponse();
                document.getElementById('chatboxInput').value = ""
            }
        });
}

// Initialization Pipelines
init();
playlistRefresh();
navButtonsListen();