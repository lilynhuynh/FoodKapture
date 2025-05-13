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

function getMealCategory() {
    let mealCategory = document.querySelector('input[name="meal-categories"]:checked');
    if (!mealCategory) {
        alert("Please select a meal category")
    }

    return mealCategory.id.replace("-opt", "");
}

if (document.body.dataset.page == 'scan') {
    startCamera(currentFacing);

    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    const title = document.getElementById('title');
    const captureButton = document.getElementById('capture-button');
    const correctButton = document.getElementById('correct-image');
    const incorrectButton = document.getElementById('incorrect-image');
    const backArrow = document.getElementById('back-arrow');
    const instructions = document.getElementById('instructions');

    captureButton.addEventListener('click', (e) => {
        e.preventDefault();

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(blob => {
            // Create a File object to mimic a file upload
            capturedFile = new File([blob], 'camera_capture.jpg', { type: 'image/jpg' });

            console.log("Blob size (bytes):", blob.size);
            console.log("Blob type:", blob.type);

            const img = new Image();
            img.onload = () => {
                console.log(`Captured image dimensions: ${img.width} x ${img.height}`);
            };
            img.src = URL.createObjectURL(blob);

            // Show preview
            const imageData = document.createElement('img');
            imageData.src = URL.createObjectURL(capturedFile);
            imageData.className = 'camera-preview';
            console.log(URL.createObjectURL(capturedFile))
            video.after(imageData);
        }, 'image/jpg');
        video.style.display = 'none';

        title.textContent = 'Confirm Photo';
        instructions.textContent = 'Please ensure that the photo is aligned in the bounding boxes'
        backArrow.style.display = 'none';

        correctButton.style.display = 'block';
        incorrectButton.style.display = 'block';
        captureButton.style.display = 'none';
    })

    incorrectButton.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.reload();
    })

    correctButton.addEventListener('click', e => {
        e.preventDefault()
        const formData = new FormData();
        const mealCategory = getMealCategory();
        console.log("Chosen meal category:", mealCategory);
        formData.append('meal_category', mealCategory);
        
        if (capturedFile) {
            formData.append('image', capturedFile)
            console.log("got input image")

        } else {
            alert("Failed to retrieve image");
        }
        console.log("new image form data", formData)

        fetch('/start_entry', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                /*
                Display results on html
                - Food classified
                - Nutritional content i.e. allergens, calories, etc.
                */
                console.log(data)
                sessionStorage.setItem('currentMeal', JSON.stringify(data));
                window.location.href = "/render_detected_page";
            })
            .catch(err => {
                console.log("Error:", err);
            });
    })
} else if (document.body.dataset.page == 'detected') {
    console.log("on detected");
    const receivedData = JSON.parse(sessionStorage.getItem("currentMeal"));

    const mealData = receivedData.output;
    console.log("Received detected items", mealData)

    const parentContainer = document.getElementById('detected-items');

    for (let key in mealData) {
        console.log(key, mealData[key])
        const mealId = `input-${key.replace(/\s+/g, '-')}`;

        let inputData = document.createElement('input');
        inputData.type = 'checkbox';
        inputData.className = 'checkbox-effect';
        inputData.id = mealId;
        inputData.value = key;
        inputData.name = key;

        let labelData = document.createElement('label');
        labelData.setAttribute('for', mealId);
        labelData.className = 'block-container';

        let checkboxItem = document.createElement('div');
        checkboxItem.className = 'checkbox-icon';

        let checkboxContainer = document.createElement('div');
        checkboxContainer.className = 'checkbox-text-container';

        let ingredientName = document.createElement('p');
        ingredientName.id = 'ingredient-name';
        ingredientName.className = 'item-text';
        ingredientName.textContent = `${key.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}`;

        let ingredientAmt = document.createElement('p');
        ingredientAmt.id = 'ingredient-amount';
        ingredientAmt.class = 'item-subtext';
        ingredientAmt.textContent = '1 serving size';

        let ingredientCals = document.createElement('p');
        ingredientCals.id = 'ingredient-calories';
        ingredientCals.class = 'item-text';

        let ingredientCalsNum = document.createElement('span');
        ingredientCalsNum.id = 'calories';
        console.log(mealData[key].calories)
        ingredientCalsNum.textContent = mealData[key].calories;
        ingredientCals.appendChild(ingredientCalsNum);

        checkboxContainer.appendChild(ingredientName);
        checkboxContainer.appendChild(ingredientAmt);
        checkboxContainer.appendChild(ingredientCals);

        labelData.appendChild(checkboxItem);
        labelData.appendChild(checkboxContainer);

        parentContainer.appendChild(inputData);
        parentContainer.appendChild(labelData);

        console.log("updated form:", parentContainer)
    }

    let logMeal = document.getElementById("submit-meal");
    logMeal.addEventListener("click", () => {
        // TODO - update sql table?
        window.location.href = "/";
    })
}
