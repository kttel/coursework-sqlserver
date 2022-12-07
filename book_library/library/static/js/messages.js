document.addEventListener('DOMContentLoaded', function () {
    hljs.highlightAll();
});


let message = document.querySelector('.message')
let messageClose = document.querySelector('.message_close')

if (message) {
    messageClose.addEventListener('click', () =>
        message.style.display = 'none'
    )
}
