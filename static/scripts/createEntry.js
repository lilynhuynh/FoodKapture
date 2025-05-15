// Will retrieve the daily entries for each meal category from SQL tables

document.addEventListener("DOMContentLoaded", () => {
    fetch('/get_daily_entries')
    .then(response => response.json())
    .then(data => {
        document.getElementById("breakfast-entries").textContent = data.breakfastNum;
        document.getElementById("lunch-entries").textContent = data.lunchNum;
        document.getElementById("dinner-entries").textContent = data.dinnerNum;
        document.getElementById("snack-entries").textContent = data.snackNum;

        let categoryMap = [ "breakfast", "lunch", "dinner", "snack" ];
        for (let category of categoryMap) { // Parse for all categories
            let parentContainer = document.querySelector(`#daily-log[data-category="${category}"`)
            let entryContainer = document.createElement("div");
            entryContainer.className = "entries-container";
            entryContainer.id = `${category}-entries-list`;

            for (var i = 0; i < data[`${category}Num`]; i++) {
                let entryItem = document.createElement("div");
                entryItem.className = "entry-item";

                let entryNum = document.createElement("h3");
                entryNum.className = "entry-number";
                entryNum.textContent = `Entry ${i+1}`
                entryItem.appendChild(entryNum);
                entryContainer.appendChild(entryItem);
            }
            parentContainer.appendChild(entryContainer)
        }
    })
    .catch(err => {
        console.error('Error occurred:', err);
    });
})

// Onload function that opens a open screen for 3 seconds
window.onload = function () {
    setTimeout(() => {
        console.log("start")
        document.getElementById('start-screen').style.display = 'none';
        document.querySelector('body').style.overflow = 'none';
    }, 3000);
};