
document.addEventListener("DOMContentLoaded", () => {
    fetch('/generate_summary_chart')
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
    })
    .catch(err => {
        console.error('Error occurred:', err);
    });
})