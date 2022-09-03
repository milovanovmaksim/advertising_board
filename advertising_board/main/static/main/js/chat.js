const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
);

chatSocket.onmessage = function(e) {
    const ads = JSON.parse(e.data).message;
    const chat_log = document.querySelector("#chat-log");
    chat_log.innerHTML = '';
    if (ads.length > 0) {
        ads.forEach(element => {
            const ad_href = element.url;
            const p = document.createElement('p');
            const link = document.createElement("a");
            link.href = ad_href;
            link.textContent = element.title;
            p.appendChild(link);
            chat_log.appendChild(p);
        });
    } else {
        p = `
            <p>Not Found</p>
        `;
        chat_log.innerHTML = p;
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};
