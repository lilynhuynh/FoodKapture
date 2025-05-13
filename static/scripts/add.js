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

servingOpen.addEventListener("click", () => {
    if (amountSheet.classList.contains("open")) {
        amountSheet.classList.remove("open");
    }
    servingSheet.classList.add("open");
});

servingClose.addEventListener("click", () => {
    servingSheet.classList.remove("open");
});

// Close on clicking outside
window.addEventListener("click", (e) => {
    if (e.target === servingSheet) {
        servingSheet.classList.remove("open");
    }
});

servingOptions.forEach(option => {
    option.addEventListener('click', () => {
        servingOpen.textContent = option.textContent;
        servingSheet.classList.remove('open');
    });
});

amountOpen.addEventListener("click", () => {
    if (servingSheet.classList.contains("open")) {
        servingSheet.classList.remove("open");
    }
    amountSheet.classList.add("open");
});

amountClose.addEventListener("click", () => {
    amountSheet.classList.remove("open");
});

// Close on clicking outside
window.addEventListener("click", (e) => {
    if (e.target === amountSheet) {
        amountSheet.classList.remove("open");
    }
});

amountOptions.forEach(option => {
    option.addEventListener('click', () => {
        amountOpen.textContent = option.textContent;
        amountSheet.classList.remove('open');
    });
});

addIngredient.addEventListener('click', (e) => {
    e.preventDefault();
    console.log("==> New ingredient entry")
    let retrievedData = JSON.parse(sessionStorage.getItem("currentMeal"));
    let mealData = retrievedData.output;

    let ingredientName = document.getElementById('ingrendient-name-entry').value;
    let ingredientServing = servingOpen.textContent;
    let ingredientAmt = amountOpen.textContent;
    let numCals = document.getElementById('calories-number').value;
    let numFats = document.getElementById('fats-number').value;
    let numCarbs = document.getElementById('carbs-number').value;
    let numProteins = document.getElementById('proteins-number').value;
    const mealName = `input-${ingredientName.replace(/\s+/g, '-')}`;

    // TODO - add serving and amt somewhere

    mealData[ingredientName] = {
        "calories": numCals,
        "carbs": numCarbs,
        "proteins": numProteins,
        "fats": numFats,
    }

    retrievedData.output = mealData;

    sessionStorage.setItem('currentMeal', JSON.stringify(retrievedData));
    // get ingredientnameentry
    // get servingsize
    // get number of servings
    // get num calories
    // get num fats
    // get num carbs
    // get num proteins
    window.location.href = '/render_detected_page';
})