



const playlist = [

{
    title: "Playlist A",
    duration: "12H 32M",
},
{
    title: "Playlist B",
    duration: "8H 14M",
},
{
    title: "Playlist C",
    duration: "5H 47M",
},
{
    title: "Playlist D",
    duration: "16H 03M",
},
{
    title: "Playlist E",
    duration: "9H 25M",
},
{
    title: "Playlist F",
    duration: "7H 58M",
},
{
    title: "Playlist G",
    duration: "11H 19M",
},
{
    title: "Playlist H",
    duration: "4H 42M",
},
{
    title: "Playlist I",
    duration: "13H 07M",
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







async function loadPlaylists() {



    const response = playlist;

    //const response = await fetch("http://127.0.0.1:5000/Playlists");  // local flask testing (flask ip)      
    
    // const response = await fetch("999.999.99.99");  // AWS backend testing (add flask ip)

    const container = document.getElementById("playlist-grid");

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

        container.appendChild(box);
        dropdownCreate('box_' + idloop)
    });

}

loadPlaylists();

iconCreate()