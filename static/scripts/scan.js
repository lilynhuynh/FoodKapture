console.log("successfully connected")

let capturedFile = null;
let currentFacing = 'environment'; // default, front-facing
let stream = null;

async function startCamera(facingMode) {
    console.log(facingMode)
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: { ideal: facingMode }
            },
            audio: false
        });
        const videoElem = document.getElementById('video')
        videoElem.srcObject = stream;
    } catch (err) {
        console.error(`Failed to start camera ${facingMode}:`, err);
    }
}

startCamera(currentFacing);


const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const title = document.getElementById('title');
const captureButton = document.getElementById('capture-button');
const correctButton = document.getElementById('correct-image');
const incorrectButton = document.getElementById('incorrect-image');
const backArrow = document.getElementById('back-arrow');

captureButton.addEventListener('click', (e) => {
    e.preventDefault();
    

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(blob => {
        // Create a File object to mimic a file upload
        capturedFile = new File([blob], 'camera_capture.png', { type: 'image/png' });

        // Show preview
        const imageData = document.createElement('img');
        imageData.src = URL.createObjectURL(capturedFile);
        imageData.className = 'camera-preview';
        console.log(URL.createObjectURL(capturedFile))
        video.after(imageData);
    }, 'image/png');
    video.style.display = 'none';

    title.textContent = 'Confirm Photo';
    backArrow.style.display = 'none';

    correctButton.style.display = 'block';
    incorrectButton.style.display = 'block';
    captureButton.style.display = 'none';
})

incorrectButton.addEventListener('click', (e) => {
    e.preventDefault();
    window.location.reload();
})

// document.getElementById('upload-form').addEventListener('submit', e => {
//     e.preventDefault()
//     const imageFile = document.getElementById('input-image')
//     console.log("got input image")
    
//     const formData = new FormData();
//     formData.append('image', imageFile.files[0])

//     console.log("new image form data", formData)

//     fetch('/classify', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         /*
//         Display results on html
//         - Food classified
//         - Nutritional content i.e. allergens, calories, etc.
//         */
//         console.log(data)
//         document.getElementById('result').innerText = JSON.stringify(data);
//     })
//     .catch(err => {
//         document.getElementById('result').innerText = 'Error: ' + err;
//     });
// })

