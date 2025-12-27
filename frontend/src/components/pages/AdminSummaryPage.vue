<script>
import { Chart } from "chart.js/auto";
import { API_BASE } from "@/api";
export default {
    name: "AdminDashboard",

    data() {
        return {
            summary: {
                total_spots: 0,
                total_available_spots: 0,
                total_reservations: 0,
                banned_users: 0,
                revenue_today: 0
            },
            pieChart: null,
            barChart: null
        };
    },

    methods: {
        // Fetch summary from backend
        fetchSummary() {
            fetch(`${API_BASE}/api/admin/summary`, {
                headers: {
                    "Token-Auth": localStorage.getItem("auth_token")
                }
            })
                .then(res => res.json())
                .then(data => {
                    this.summary = data;
                    this.renderPieChart();
                    this.renderBarChart();
                })
                .catch(err => console.error("Summary API Error:", err));
        },

        // Pie chart: Available vs Occupied
        renderPieChart() {
            if (this.pieChart) this.pieChart.destroy();

            const occupied = this.summary.total_spots - this.summary.total_available_spots;

            this.pieChart = new Chart(document.getElementById("spotsPieChart"), {
                type: "pie",
                data: {
                    labels: ["Available Spots", "Occupied Spots"],
                    datasets: [{
                        data: [this.summary.total_available_spots, occupied],
                        backgroundColor: ["#4CAF50", "#F44336"]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: "bottom",
                            labels: {
                                font: {
                                    size: 16,   
                                    weight: "bold"  
                                },
                                color: "#000"  
                            }
                        }
                    }
                }
            });
        },

        renderBarChart() {
            if (this.barChart) this.barChart.destroy();

            this.barChart = new Chart(document.getElementById("summaryBarChart"), {
                type: "bar",
                data: {
                    labels: ["Reservations", "Banned Users", "Revenue Today"],
                    datasets: [{
                        label: "Summary Data",
                        data: [
                            this.summary.total_reservations,
                            this.summary.banned_users,
                            this.summary.revenue_today
                        ],
                        backgroundColor: ["#2196F3", "#E91E63", "#9C27B0"]
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }
    },

    mounted() {
        this.fetchSummary();
    }
};
</script>

<template>
    <div class="dashboard">

        <h2 class="text-center mt-3">Admin Dashboard</h2>

        <!-- Summary Cards -->
        <div class="cards">
            <div class="card">
                <h4>Total Spots</h4>
                <p>{{ summary.total_spots }}</p>
            </div>

            <div class="card">
                <h4>Available Spots</h4>
                <p>{{ summary.total_available_spots }}</p>
            </div>

            <div class="card">
                <h4>Total Reservations</h4>
                <p>{{ summary.total_reservations }}</p>
            </div>

            <div class="card">
                <h4>Revenue Today</h4>
                <p>₹ {{ summary.revenue_today }}</p>
            </div>
        </div>

        <!-- Charts -->
        <div class="charts">

            <div class="chart-box">
                <h4>Available vs Occupied</h4>
                <canvas id="spotsPieChart"></canvas>
            </div>

            <div class="chart-box">
                <h4>Summary Overview</h4>
                <canvas id="summaryBarChart"></canvas>
            </div>
        </div>

    </div>
</template>

<style scoped>
.dashboard {
    width: 90%;
    margin: auto;
}

/* Summary Cards */
.cards {
    display: flex;
    justify-content: space-between;
    margin: 20px 0;
}

.card {
    width: 23%;
    background: #3bd9d9;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
     font-weight: bold;
}
.card:hover {
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    transform: translateY(-8px);
    transition: all 0.5s ease;
    background-color: #3bd946;
   
}

/* Charts Layout */
.charts {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
}

.chart-box {
    width: 40rem;
    height: 30rem;
    padding: 20px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

#spotsPieChart{
    margin-top: 50px;
    width: 60% !important;
    height: 70% !important;
}
#summaryBarChart {
    margin-top: 50px;
    width: 80% !important;
    height: 70% !important;
}
</style>

