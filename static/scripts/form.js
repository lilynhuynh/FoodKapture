console.log("successfully connected")

document.getElementById('upload-form').addEventListener('submit', e => {
    e.preventDefault()
    const imageFile = document.getElementById('input-image')
    console.log("got input image")
    
    const formData = new FormData();
    formData.append('image', imageFile.files[0])

    console.log("new image form data", formData)

    fetch('/classify', {
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
        document.getElementById('result').innerText = JSON.stringify(data);
    })
    .catch(err => {
        document.getElementById('result').innerText = 'Error: ' + err;
    });
})

