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


async function updateSensorReadings() {
    try {
        const response = await fetch("/api/readings/latest");

        if (!response.ok) {
            throw new Error("Failed to retrieve sensor readings");
        }

        const reading = await response.json();

        document.getElementById("temperatureValue").textContent =
            `${reading.temperature.toFixed(1)} °C`;

        document.getElementById("humidityValue").textContent =
            `${reading.humidity.toFixed(1)}%`;

        const recordedTime = new Date(reading.recorded_at);

        document.getElementById("sensorUpdateTime").textContent =
            `Last simulated reading: ${recordedTime.toLocaleString("en-GB", {
                timeZone: "Africa/Lagos"
            })} (WAT)`;

    } catch (error) {
        console.error("Sensor reading error:", error);

        document.getElementById("sensorUpdateTime").textContent =
            "Unable to retrieve sensor readings";
    }
}


async function updateSensorStatus() {
    try {
        const response = await fetch("/api/sensors/status");

        if (!response.ok) {
            throw new Error("Failed to retrieve sensor status");
        }

        const sensor = await response.json();

        document.getElementById("sensorStatus").textContent =
            sensor.status;

        const details = document.getElementById("sensorStatusDetails");

        if (sensor.status === "Reporting") {
            details.textContent =
                `Latest reading received ${sensor.seconds_since_reading.toFixed(1)} seconds ago.`;
        } else if (sensor.status === "Not reporting") {
            details.textContent =
                `No new reading for ${sensor.seconds_since_reading.toFixed(1)} seconds.`;
        } else {
            details.textContent =
                "No readings have been recorded for this sensor.";
        }

    } catch (error) {
        console.error("Sensor status error:", error);

        document.getElementById("sensorStatus").textContent =
            "Unavailable";

        document.getElementById("sensorStatusDetails").textContent =
            "Unable to check sensor status.";
    }
}

updateSensorStatus();

setInterval(updateSensorStatus, 5000);

updateSensorReadings();

setInterval(updateSensorReadings, 5000);

