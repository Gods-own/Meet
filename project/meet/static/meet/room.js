function scrollToBottom() {
    let objDiv = document.getElementById("chat-messages");
    objDiv.scrollTop = objDiv.scrollHeight;
}

scrollToBottom()

const roomName = JSON.parse(document.getElementById('json-roomname').textContent);
const userName = JSON.parse(document.getElementById('json-username').textContent);
const userid1 = JSON.parse(document.getElementById('json-userid1').textContent);
const userid2 = JSON.parse(document.getElementById('json-userid2').textContent);


let loc = window.location
let wsStart;
let mStart = '/ws/'
let message = 'message/'

if (loc.protocol === 'https') {
    wsStart = 'wss://'
}
else {
    wsStart = 'ws://'
}
let endpoint = wsStart + loc.host + mStart + message + userid2 + '/' + roomName

const chatSocket = new WebSocket(endpoint + '/')


// chatSocket.onopen = function(e) {
//     console.log('opened', e)
//     fetch("/notification/"+userid2, {
//         method: 'PUT',
//         body: JSON.stringify({
//             notification_read: true
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log(data)
//     })
// }

chatSocket.onmessage = function(e) {
    console.log('message', e)

    const data = JSON.parse(e.data);
    console.log(data)
    if (data.message) {

        if(data.checkuser == true) {
            document.querySelector('#chat-messages').innerHTML += `
            <div class="msg-box chat-right">
        <img class="msg-box-img" src="${data.get_extra_info.userImage}">
        <div class="msg-box-div">
            <h4>${data.username}</h4>
            <pre>${data.message}</pre>
            <small>${data.get_extra_info.date_added}</small>
        </div>
    </div>

     <div class="clear"></div>`

     document.querySelector('.notification').innerHTML = data.get_notifications;
        }
        else {
            document.querySelector('#chat-messages').innerHTML += `
            <div class="msg-box chat-left">
        <img class="msg-box-img" src="${data.get_extra_info.userImage}">
        <div class="msg-box-div">
            <h4>${data.username}</h4>
            <pre>${data.message}</pre>
            <small>${data.get_extra_info.date_added}</small>
        </div>
    </div>

     <div class="clear"></div>`
        }
        // console.log(data.connected_users)
        if(data.connected_users == 2) {
            fetch("/notification/"+userid2, {
                method: 'PUT',
                body: JSON.stringify({
                    notification_read: true
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
            })
        }
    }
    else {
        alert('The message is empty')
    }

    scrollToBottom();
    
}

// chatSocket.onclose = function(e) {
//     alert('The socket closed unexpectedly')
//     fetch("/notification/"+userid2, {
//         method: 'PUT',
//         body: JSON.stringify({
//             notification_read: true
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log(data)
//     })
// }

document.querySelector('.form-message').addEventListener('submit', function(e) {
    e.preventDefault()
    const messageInputDom = document.querySelector('#chat-message-input')
    const message = messageInputDom.value;

    chatSocket.send(JSON.stringify({
        'message': message,
        'username': userName,
        'room': roomName,
        'user1': userid1,
        'user2': userid2
    }))

    messageInputDom.value = '';
})

