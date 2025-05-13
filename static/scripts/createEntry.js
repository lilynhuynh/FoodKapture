console.log("successfully connected")

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

// document.querySelectorAll('.meal-entry').forEach(div => {
//     div.addEventListener('click', () => {
//         const category = div.getAttribute("data-category")
//         console.log("==> New request for", category)

//         const formData = new FormData();
//         formData.append('meal_category', category);
        
//         // Debug formData
//         for (let [key, value] of formData.entries()) {
//             console.log(`${key}: ${value}`);
//         }

//         fetch('/start_entry', {
//             method: 'POST',
//             body: formData
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error(`HTTP ${response.status}`);
//             }
//             return response.json();
//         })
//         .then(data => {
//             console.log("==> Successfully received new entry:", data);


//             document.getElementById("breakfast-entries").textContent = data.breakfastNum;
//             document.getElementById("lunch-entries").textContent = data.lunchNum;
//             document.getElementById("dinner-entries").textContent = data.dinnerNum;
//             document.getElementById("snack-entries").textContent = data.snackNum;
//         })
//         .catch(err => {
//             console.error('Error occurred:', err);
//         });
//     })
// })

window.onload = function () {
    setTimeout(() => {
        console.log("start")
        document.getElementById('start-screen').style.display = 'none';
        document.querySelector('body').style.overflow = 'none';
    }, 3000);
};

// 3000 x 4000 pixels minimum