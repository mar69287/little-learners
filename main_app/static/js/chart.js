// Import Chart.js
import Chart from 'chart.js/auto';

// Get the canvas element
const canvas = document.getElementById('attendance-chart');

// Get the attendance data from the HTML template
const data = JSON.parse(canvas.getAttribute('data-attendance'));

// Create the chart
new Chart(canvas, {
    type: 'pie',
    data: {
        labels: ['Present', 'Absent'],
        datasets: [{
            data: [data.present, data.absent],
            backgroundColor: ['green', 'red']
        }]
    }
});


