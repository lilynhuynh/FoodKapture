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
