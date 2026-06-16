// Global Confguration
const BACKEND_ADDRESS = window.location.origin;
// All fetch requests MUST have /api appended to the address or else it will not reach the flask 
// -backend due to behavior restrictions from cloudfront.
const playlist = [];

const paths = {
  userIcon: "assets/userIcon.svg",
  menuUp: "assets/arrowUp.svg",
  menuDown: "assets/arrowDown.svg",
  sendButton: "assets/send.svg",
};

// State Elements
const username = document.getElementById("userName");

// ==========================================
// UI Components
// ==========================================

function sendButtonCreate() {
  const chatbox = document.getElementById("chatbot-input-button");
  if (!chatbox) {
    console.log("chatbot-input-button not found");
    return;
  }

  const sendButton = document.createElement("img");
  sendButton.src = paths.sendButtonPath;
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
  userIcon.src = paths.userIconPath;
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
  dropdown.src = paths.menuDownPath;
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

async function loadPlaylists() {
  const playlistContainer = document.getElementById("playlist-grid");
  if (!playlistContainer) {
    console.log("playlist-grid not found");
    return;
  }

  playlistContainer.innerHTML = "";
  const playlists = await playlistFetchFlask();

  playlists.forEach((playlist, index) => {
    const boxId = `box_${index + 1}`;
    const cardbox = document.createElement("div");
    cardBox.className = "playlist-item";
    cardBox.id = boxId;

    let contentStructure = "";
    if (playlist.title) {
      contentStructure += `<h3>${playlist.title}</h3>`;
    }
    if (playlist.duration) {
      contentStructure += `<p>Duration: ${playlist.duration}</p>`;
    }

    cardBox.innerHTML = contentStructure;
    playlistContainer.appendChild(cardBox);
    dropdownCreate(boxId);
  });
}

// ==========================================
// Dialogue & Interface
// ==========================================

async function loadChat(text, alignmentId) {
  // This is for loading previous chats, it takes an input from flask
  const chatContainer = document.getElementById("chatboxWindow");
  if (!chatContainer) {
    console.log("playlist-grid not found");
    return;
  }

  const chatItem = document.createElement("p");
  chatItem.className = "chat-item";
  chatItem.textContent = text;

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
  const chatInput = document.getElementById("chatboxinput");
  if (!chatInput) {
    console.log("chatboxinput not found");
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

    const chatInput = document.getElementById("chatboxinput");
    if (chatInput) chatInput.value = "";

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
    });
  if (infoButton)
    infoButton.addEventListener("click", () => {
      console.log("info button clicked");
    });
  if (loginButton)
    loginButton.addEventListener("click", () => {
      console.log("login button clicked");
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
  if (username) username.textContent = "George";
}

// refreshes the playlists, in a function for when additional functionality required
async function playlistRefresh() {
  loadPlaylists();
}

// async function infoPopup() {

// }

function textAreaHandler() {
  document.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      const chatInput = document.getElementById("chatboxinput");
      if (chatInput && document.activeElement === chatInput) {
        event.preventDefault();
        flaskChatSendResponse();
      }
    }
  });
}

// Initialization Pipelines
init();
playlistRefresh();
navButtonsListen();