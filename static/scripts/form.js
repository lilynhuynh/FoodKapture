const formData = new FormData();
formData.append('image', imageFile)

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
})