<template>
    <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger','text-center'] " role="alert">
  {{ message }}
</div>

    <div>
        <!-- Active Spots Chart -->
        <div v-if="Object.keys(countLoc).length">
            <h1 class="text-center mt-5 mb-0">Active Spots</h1>
            <div class="container room-container">
                <canvas id="SpotsChart"></canvas>
            </div>
        </div>

        <!-- Duration Chart -->
        <div v-if="data.length">
            <h1 class="text-center mt-5 mb-0">Total Duration of Individual Location</h1>
            <div class="container room-container">
                <canvas id="durationChart2"></canvas>
            </div>
        </div>
    </div>
</template>

<script>
import { Chart } from "chart.js/auto";


export default {
    name: "SummaryPage",

    data() {
        return {
            userData: {},
            data: [],
            countLoc: {},
        };
    },
    mounted() {
        const token = localStorage.getItem("auth_token");

        fetch("http://localhost:5000/api/user/user_summary", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Token-Auth": token,
            },
        })
            .then((response) => response.json())
            .then((result) => {
                console.log(result);
                this.data = result.data || [];
                this.countLoc = result.count_loc || {};
                this.userData = result.user_data || {};

                this.$nextTick(() => {
                    this.renderSpotsChart();
                    this.renderDurationChart();
                });
            })
            .catch((error) => {
                console.error("Error loading summary:", error);
            });
    },
    methods: {
        renderSpotsChart() {
            if (!Object.keys(this.countLoc).length) return;

            const ctx = document.getElementById("SpotsChart").getContext("2d");
            ctx.width = 1000;
            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: Object.keys(this.countLoc),
                    datasets: [
                        {
                            label: "Active Spots Count",
                            data: Object.values(this.countLoc),
                            backgroundColor: ["#228B22"],
                            barThickness: 60,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    plugins: { legend: { position: "top" } },
                    scales: { y: { beginAtZero: true } },
                },
            });
        },

        renderDurationChart() {
            if (!this.data.length) return;

            const ctx2 = document.getElementById("durationChart2").getContext("2d");
            ctx2.width = 1000;
            const labels = this.data.map((item) => item.prime_location);
            const durations = this.data.map((item) => item.total_duration);
            console.log("Chart Labels:", labels);
            console.log("durations", durations);
            new Chart(ctx2, {
                type: "bar",
                data: {
                    labels,
                    datasets: [
                        {
                            label: "Total Duration Per Location",
                            data: durations,
                            backgroundColor: "rgba(153, 102, 255, 0.6)",
                            borderColor: "rgba(153, 102, 255, 1)",
                            borderWidth: 1,
                            barThickness: 60,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    indexAxis: "y",
                    plugins: {
                        legend: { position: "bottom" },
                        tooltip: {
                            callbacks: {
                                label: (context) => {
                                    const item = this.data[context.dataIndex];
                                    return `Location: ${item.prime_location}\nDuration: ${item.total_duration} hrs`;
                                },
          },
        },
      },
                        scales: {
                            x: { beginAtZero: true },
                            y: { ticks: { autoSkip: false } },
                        },
                    },
                });
        },
    },
};
</script>

<style scoped>
.room-container {
    width: 50%;
    height: 100%;
    display: flex;
    margin-top: 4rem;
    justify-content: center;
    flex-direction: column;
    align-items: center;
}
</style>
