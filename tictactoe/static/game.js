socket = io();

for (let html_tile of document.getElementsByClassName("tile")) {
    html_tile.addEventListener("click", (event) => {
        // Extract the coordinates from tile
        let coords = event.target.id;
        let x = coords[0];
        let y = coords[1];

        console.log("button pressed at", x, y);
      
        // TODO
        socket.emit("place_tile", {"x": coords[0], "y": coords[1]});
    });
}

// TODO
socket.on("placed_tile", (data) => {
    draw(data["board"]);
});


socket.on("connect", () => {
    socket.emit("join_game");
});

socket.on("joined_game", (data) => {
    draw(data["board"]);
    write_to_right_display(data["is_waiting"] ? "Waiting for an opponent" : "Playing!!!");
});

socket.on("disconnected", () => {
    write_to_right_display("Game over: other player disconnected");
})

function write_to_left_display(message) {
    let left_display = document.getElementById("left_display");
    left_display.textContent = message;
}

function write_to_right_display(message) {
    let right_display = document.getElementById("right_display");
    left_display.textContent = message;
}

function draw(board) {
    for (let x = 0; x < 3; x++) {
        for (let y = 0; y < 3; y++) {
            let html_tile = document.getElementById("tile_" + x + y);
            html_tile.textContent = board[x][y];
        }
    }
}
