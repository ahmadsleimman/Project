
const userId = JSON.parse(document.getElementById('user').textContent);
const class_id = JSON.parse(document.getElementById('class_id').textContent);
const class_name = JSON.parse(document.getElementById('class_name').textContent);

const chatSocket = new WebSocket(`ws://${window.location.host}/ws/${class_id}/`);

chatSocket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    if (data) {
        if (data.message_type === "message") {
            displayMessage(data);
        }
        if (data.message_type === "voice") {
            displayVoice(data);
        }
        if (data.message_type === "image") {
            displayImage(data);
        }
    }
    scrollBottom();
}

document.querySelector('#chat-message-submit').onclick = (e) => {
    e.preventDefault();

    const messageInputDom = document.querySelector('#chat-message-input');
    const body = messageInputDom.value;
    if (body.length > 0) {
        chatSocket.send(JSON.stringify({
            'message_type': "message",
            'body': body,
            'user': userId,
        }));
    }
    messageInputDom.value = '';
};


function scrollBottom() {
    let objDiv = document.querySelector("#chat1 .card-body");
    objDiv.scrollTop = objDiv.scrollHeight;
}

scrollBottom();

const imgFile = document.querySelector('#image-file');
const imgFileHandler = document.querySelector('#image-file-handler');

imgFileHandler.addEventListener('click', (e) => {
    e.preventDefault();
    imgFile.click();
});

imgFile.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (file) {
        try {
            const base64String = await readFileAsBase64(file);
            chatSocket.send(JSON.stringify({
                'message_type': 'image',
                'image': base64String,
                'image_name': file.name,
                'image_type': file.type,
                'user': userId,
            }));
            imgFile.value = "";
        } catch (error) {
            console.error('Error reading file:', error);
        }
    }
});


function readFileAsBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
            const base64String = reader.result.split(',')[1];
            resolve(base64String);
        };
        reader.onerror = error => reject(error);
        reader.readAsDataURL(file);
    });
}

const displayMessage = (data) => {
    let html = ``;
    if (userId == data.user) {
        html = `
            <div class="d-flex flex-row justify-content-end my-2">
                <div>
                    <small class="mb-2 rounded-3 text-muted d-flex justify-content-end">@me</small>
                    <p class="p-2 mb-1 text-white rounded-3 bg-primary">${data.body}</p>
                    <small class="mb-3 rounded-3 text-muted d-flex justify-content-end">${data.created}</small>
                </div>
            </div>`
    } else {
        html = `
            <div class="d-flex flex-row justify-content-start my-2">
                <div>
                    <small class="mb-2 rounded-3 text-muted">@${data.name}</small>
                    <p class="p-2 mb-1 rounded-3" style="background-color: #f5f6f7;">${data.body}</p>
                    <small class="mb-3 rounded-3 text-muted">${data.created}</small>
                </div>
            </div>`
    }
    const newChatElement = document.createElement("div");
    newChatElement.innerHTML = html;
    document.querySelector("#chat1 .card-body").appendChild(newChatElement);
}

const displayVoice = (data) => {
    const voice = data.voice;
    let html = ``;
    if (userId == data.user) {
        html = `
            <div class="d-flex flex-row justify-content-end my-2">
                <div>
                    <small class="mb-2 rounded-3 text-muted d-flex justify-content-end">@me</small>
                    <div class="mb-1">
                        <audio controls controlsList="nodownload">
                            <source src="data:audio/mp3;base64,${voice}" type="audio/mp3">
                            Your browser does not support the audio element.
                        </audio>
                    </div>
                    <small class="mb-3 rounded-3 text-muted d-flex justify-content-end">${data.created}</small>
                </div>
            </div>`;
    } else {
        html = `
            <div class="d-flex flex-row justify-content-start my-2">
                <div>
                    <small class="mb-2 rounded-3 text-muted">@${data.name}</small>
                    <div class="mb-1">
                        <audio controls controlsList="nodownload">
                            <source src="data:audio/mp3;base64,${voice}" type="audio/mp3">
                            Your browser does not support the audio element.
                        </audio>
                    </div>
                    <small class="mb-3 rounded-3 text-muted">${data.created}</small>
                </div>
            </div>`
    }
    const newChatElement = document.createElement("div");
    newChatElement.innerHTML = html;
    document.querySelector("#chat1 .card-body").appendChild(newChatElement);
}

const displayImage = (data) => {
    const image = data.image;
    const imageType = data.image_type;
    let html = ``;
    if (userId == data.user) {
        html = `
            <div class="d-flex flex-row justify-content-end my-2">
                <div>
                    <small class="mb-2 rounded-3 text-muted d-flex justify-content-end">@me</small>
                    <div class="mb-1">
                        <a href="data:${imageType};base64,${image}" data-lightbox="CLASS${class_id}">
                            <img class="img-fluid" width="300px" src="data:${imageType};base64,${image}" alt="image">
                        </a>
                    </div>
                    <small class="mb-3 rounded-3 text-muted d-flex justify-content-end">${data.created}</small>
                </div>
            </div>`;
    } else {
        html = `
            <div class="d-flex flex-row justify-content-start my-2">
                <div>
                    <small class="mb-2 rounded-3 text-muted">@${data.name}</small>
                    <div class="mb-1">
                        <a href="data:${imageType};base64,${image}" data-lightbox="CLASS${class_id}">
                            <img class="img-fluid" width="300px" src="data:${imageType};base64,${image} alt="image">
                        </a>
                    </div>
                    <small class="mb-3 rounded-3 text-muted">${data.created}</small>
                </div>
            </div>`
    }
    const newChatElement = document.createElement("div");
    newChatElement.innerHTML = html;
    document.querySelector("#chat1 .card-body").appendChild(newChatElement);
}


const startRecord = document.getElementById("startRecord");
const stopRecord = document.getElementById("stopRecord");
const deleteRecord = document.getElementById("deleteRecord");
let mediaRecorder;
let chunks = [];

startRecord.addEventListener("click", (e) => {
    e.preventDefault();
    handleStartRecord();
});

stopRecord.addEventListener("click", (e) => {
    e.preventDefault();
    handleStopRecord();
});

deleteRecord.addEventListener("click", (e) => {
    e.preventDefault();
    handleDeleteRecord();
});

const handleStartRecord = () => {

    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {

        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (e) => chunks.push(e.data);

        mediaRecorder.onstop = async () => {
            try {
                const options = { type: "audio/mp3" };
                const audioBlob = new Blob(chunks, options);
                const base64String = await readFileAsBase64(audioBlob);

                chatSocket.send(JSON.stringify({
                    'message_type': 'voice',
                    'voice': base64String,
                    'voice_name': `CLASS${userId}${Date.now()}`,
                    'user': userId,
                }));

                chunks = [];

                if (mediaRecorder && mediaRecorder.stream) {
                    mediaRecorder.stream.getTracks().forEach(track => track.stop());
                    mediaRecorder.stream = null;
                }
            } catch (error) {
                console.error('Error reading file:', error);
            }
        };

        mediaRecorder.start();
        startRecord.classList.toggle("d-none");
        stopRecord.classList.toggle("d-none");
        deleteRecord.classList.toggle("d-none");
    });
};


const handleStopRecord = () => {
    if (mediaRecorder) {
        mediaRecorder.stop();
        mediaRecorder = null;
        startRecord.classList.toggle("d-none");
        stopRecord.classList.toggle("d-none");
        deleteRecord.classList.toggle("d-none");
    }
};


const handleDeleteRecord = () => {
    if (mediaRecorder) {
        chunks = [];
        mediaRecorder = null;
        startRecord.classList.toggle("d-none");
        stopRecord.classList.toggle("d-none");
        deleteRecord.classList.toggle("d-none");
    }
};