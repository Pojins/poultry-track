const chartCanvas = document.getElementById("environmentChart");

const chartData = {
    labels: ["06:00", "08:00", "10:00", "12:00", "14:00", "14:30"],

    datasets: [
        {
            label: "Temperature (°C)",
            data: [26, 27, 29, 30, 32, 32],
            borderColor: "#333333",
            backgroundColor: "#333333",
            tension: 0.3,
            yAxisID: "temperatureAxis"
        },
        {
            label: "Humidity (%)",
            data: [86, 84, 82, 80, 78, 78],
            borderColor: "#999999",
            backgroundColor: "#999999",
            tension: 0.3,
            yAxisID: "humidityAxis"
        }
    ]
};

new Chart(chartCanvas, {
    type: "line",
    data: chartData,

    options: {
        responsive: true,
        maintainAspectRatio: false,

        plugins: {
            legend: {
                position: "top"
            },
            title: {
                display: false
            }
        },

        scales: {
            temperatureAxis: {
                type: "linear",
                position: "left",
                title: {
                    display: true,
                    text: "Temperature (°C)"
                }
            },

            humidityAxis: {
                type: "linear",
                position: "right",
                title: {
                    display: true,
                    text: "Humidity (%)"
                },
                grid: {
                    drawOnChartArea: false
                }
            }
        }
    }
});
