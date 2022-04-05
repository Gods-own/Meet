// document.querySelector(".room-form").addEventListener('submit', function(e) {
//     e.preventDefault()
    
//     var roomName = document.querySelector("#room-name-input").value;
//     var userName = document.querySelector("#username-input").value;

//     window.location.replace(roomName+'hey')
// })

document.querySelector(".messagebtn").addEventListener('click', function() {

    let roomName = JSON.parse(document.getElementById('json-roomName').textContent);
    let userid1 = JSON.parse(document.getElementById('json-userid1').textContent);
    let userid2 = JSON.parse(document.getElementById('json-userid2').textContent);   
    let username1 = JSON.parse(document.getElementById('json-username1').textContent);
    let username2 = JSON.parse(document.getElementById('json-username2').textContent);
    if (roomName == "generate") {
        let a = Math.round(Math.random() * 9)
        let b = Math.round(Math.random() * 9)
        let c = Math.round(Math.random() * 9)
        
        username1 = username1.charAt(1)
        username2 = username2.charAt(1)
        roomName = `${username1}${username2}${userid1}${userid2}${a}${b}${c}`
    } else {
        roomName = roomName
    }

    window.location.replace('/'+'message'+'/'+userid2+'/'+roomName)
})