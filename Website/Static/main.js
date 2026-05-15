



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
{
    title: "Playlist J",
    duration: "6H 31M",
},
{
    title: "Playlist K",
    duration: "15H 49M",
},
{
    title: "Playlist L",
    duration: "10H 12M",
},
{
    title: "Playlist M",
    duration: "3H 56M",
},
{
    title: "Playlist N",
    duration: "14H 28M",
},
{
    title: "Playlist O",
    duration: "2H 44M",
},
{
    title: "Playlist P",
    duration: "18H 11M",
},
{
    title: "Playlist Q",
    duration: "5H 09M",
},
{
    title: "Playlist R",
    duration: "12H 50M",
},
{
    title: "Playlist S",
    duration: "9H 37M",
},
{
    title: "Playlist T",
    duration: "7H 15M",
},
{
    title: "Playlist U",
    duration: "6H 53M",
},
{
    title: "Playlist V",
    duration: "17H 26M",
},
{
    title: "Playlist W",
    duration: "8H 41M",
},
{
    title: "Playlist X",
    duration: "4H 18M",
},
{
    title: "Playlist Y",
    duration: "13H 55M",
},
{
    title: "Playlist Z",
    duration: "11H 04M",
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