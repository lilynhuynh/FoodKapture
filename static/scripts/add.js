// JavaScript logic for Add Ingredient page

const addIngredient = document.getElementById('submit-ingredient');
console.log(addIngredient);
console.log(JSON.parse(sessionStorage.getItem('currentMeal')));

// SERVING SIZE
const servingOpen = document.getElementById("serving-size-entry");
const servingClose = document.getElementById("serving-size-close-sheet");
const servingSheet = document.getElementById("serving-size-bottom-sheet");
const servingOptions = document.querySelectorAll('#serving-item')

// AMOUNT SIZE
const amountOpen = document.getElementById("amount-size-entry");
const amountClose = document.getElementById("amount-size-close-sheet");
const amountSheet = document.getElementById("amount-size-bottom-sheet");
const amountOptions = document.querySelectorAll("#amount-item");

// Listens for when user clicks to add serving size
servingOpen.addEventListener("click", () => {
    if (amountSheet.classList.contains("open")) {
        amountSheet.classList.remove("open");
    }
    servingSheet.classList.add("open");
});

// Listens for when user closes the serving size popup
servingClose.addEventListener("click", () => {
    servingSheet.classList.remove("open");
});

// Close serving size popup on clicking outside
window.addEventListener("click", (e) => {
    if (e.target === servingSheet) {
        servingSheet.classList.remove("open");
    }
});

// If a user chooses a option from the serving size popup, set the text container to the chosen option
servingOptions.forEach(option => {
    option.addEventListener('click', () => {
        servingOpen.textContent = option.textContent;
        servingSheet.classList.remove('open');
    });
});

// Listens for when user clicks to add amount
amountOpen.addEventListener("click", () => {
    if (servingSheet.classList.contains("open")) {
        servingSheet.classList.remove("open");
    }
    amountSheet.classList.add("open");
});

// Listens for when user closes the amount popup
amountClose.addEventListener("click", () => {
    amountSheet.classList.remove("open");
});

// Close amount popup on clicking outside
window.addEventListener("click", (e) => {
    if (e.target === amountSheet) {
        amountSheet.classList.remove("open");
    }
});

// If a user chooses a option from the amount popup, set the text container to the chosen option
amountOptions.forEach(option => {
    option.addEventListener('click', () => {
        amountOpen.textContent = option.textContent;
        amountSheet.classList.remove('open');
    });
});

// When user clicks on Add Ingredient button, it will store the new ingredient in sessionStorage to be accessed later
addIngredient.addEventListener('click', (e) => {
    e.preventDefault();
    console.log("==> New ingredient entry")
    let retrievedData = JSON.parse(sessionStorage.getItem("currentMeal"));
    let mealData = retrievedData.output;

    let ingredientName = document.getElementById('ingrendient-name-entry').value;
    let ingredientAmt = amountOpen.textContent;
    let numCals = document.getElementById('calories-number').value.toLowerCase();
    let numFats = document.getElementById('fats-number').value;
    let numCarbs = document.getElementById('carbs-number').value;
    let numProteins = document.getElementById('proteins-number').value;
    const mealName = `input-${ingredientName.replace(/\s+/g, '-')}`;

    mealData[ingredientName] = {
        "calories": parseInt(numCals),
        "carbs": parseInt(numCarbs),
        "proteins": parseInt(numProteins),
        "fats": parseInt(numFats),
        "amount": parseInt(ingredientAmt)
    }

    retrievedData.output = mealData;

    sessionStorage.setItem('currentMeal', JSON.stringify(retrievedData));
    window.location.href = '/render_detected_page';
})