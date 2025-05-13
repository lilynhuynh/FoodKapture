
document.addEventListener("DOMContentLoaded", () => {
    const mealData = JSON.parse(sessionStorage.getItem('currentMeal')).output;
    console.log(mealData);
    
    fetch('/generate_summary_chart', {
        method: 'POST',
        body: JSON.stringify({ output: mealData})
    })
    .then(response => response.json())
    .then(data => {
        const context = document.getElementById('summary-chart');
        context.getContext('2d');

        new Chart(context, {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Data',
                    data: data.values,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });

        const totalCals = document.getElementById('total-calories');
        const totalFats = document.getElementById('total-fats');
        const totalProteins = document.getElementById('total-proteins');
        const totalCarbs = document.getElementById('total-carbs');

        totalCals.textContent = data.cals;
        totalFats.textContent = data.fats;
        totalCarbs.textContent = data.carbs;
        totalProteins.textContent = data.proteins;


    })
    .catch(err => {
        console.error('Error occurred:', err);
    });
})