document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        // Each button should emit a "submit vote" event
        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                const selection = button.dataset.vote;
                socket.emit('submit vote', {'selection': selection});
            };
        });
      
        // Add an event listener for the input field
        let input = document.getElementById('chat');
        input.onkeydown = (event) => {
          if(event.key === 'Enter') {
             socket.emit('messaged', {'message': input.value});
            input.value = '';
          }
        }
    });

    // When a new vote is announced, add to the unordered list
    socket.on('vote totals', data => {
        document.querySelector('#yes').innerHTML = data.yes;
        document.querySelector('#no').innerHTML = data.no;
        document.querySelector('#maybe').innerHTML = data.maybe;
    });
  
    // When a new message has been sent, update message display
    socket.on('display', data => {
      document.getElementById('text-display').textContent = data;
    })
  
});
