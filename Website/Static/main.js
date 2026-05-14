function icon_create(){
    const userIcon = document.createElement("img");
    userIcon.src = "assets/userIcon.svg";
    userIcon.alt = "User icon";
    userIcon.style.width = '100%'
    userIcon.style.height = '100%'
    document.getElementById("userIcon").appendChild(userIcon);
}

const songs = [
    {
        title: "Song A",
        artist: "Artist 1",
        duration: "3:24",
        genre: "Rock"
    },
    {
        title: "Song B",
        artist: "Artist 2",
        duration: "4:10",
        genre: "Pop"
    },
    {
        title: "Song C",
        artist: "Artist 3",
        duration: "2:58",
        genre: "Electronic"
    },
    {
        title: "Song D",
        artist: "Artist 4",
        duration: "5:01",
        genre: "Jazz"
    },
    {
    title: "Song E",
    artist: "Artist 5",
    duration: "3:42",
    genre: "Rock"
    },
    {
        title: "Song F",
        artist: "Artist 6",
        duration: "4:18",
        genre: "Pop"
    },
    {
        title: "Song G",
        artist: "Artist 7",
        duration: "2:55",
        genre: "Hip Hop"
    },
    {
        title: "Song H",
        artist: "Artist 8",
        duration: "6:03",
        genre: "Electronic"
    }
];

async function loadSongs() {



    const response = songs;

    //const response = await fetch("http://127.0.0.1:5000/songs");  // local flask testing (flask ip)      
    
    // const response = await fetch("999.999.99.99");  // AWS backend testing (add flask ip)

    const container = document.getElementById("playlist-grid");

    songs.forEach(song => {

        const box = document.createElement("div");

        box.className = "playlist-item";

        box.innerHTML = `
            <h1>${song.title}</h1>
            <p>${song.artist}</p>
            <p>${song.duration}</p>
            <p>${song.genre}</p>
        `;

        container.appendChild(box);

    });

}

loadSongs();

icon_create()