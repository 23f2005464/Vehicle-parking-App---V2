

<script>
import { API_BASE } from "@/api";    
import { Chart } from "chart.js/auto";

export default {
    name: "SummaryPage",

    data() {
        return {
            userData: {},
            data: [],
            countLoc: {},
            message:'',
            messageType:''
        };
    },

    mounted() {
        const token = localStorage.getItem("auth_token");

        fetch(`${API_BASE}/api/user/user_summary`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Token-Auth": token,
            },
        })
            .then((response) => response.json())
            .then((result) => {
                if (result.message){
                    this.message=result.message
                    this.messageType='danger'
                    return
                }
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
        /** Utility to generate random colors for each bar */
        generateColors(length) {
            const colors = [];
            for (let i = 0; i < length; i++) {
                const r = Math.floor(Math.random() * 255);
                const g = Math.floor(Math.random() * 255);
                const b = Math.floor(Math.random() * 255);
                colors.push(`rgba(${r}, ${g}, ${b}, 0.8)`);
            }
            return colors;
        },

        /** Animation delay per bar for smooth effect */
        barAnimationDelay(context) {
            let delay = 0;
            if (context.type === "data" && context.mode === "default") {
                delay = context.dataIndex * 150; // 150ms stagger animation
            }
            return delay;
        },

        renderSpotsChart() {
            if (!Object.keys(this.countLoc).length) return;

            const labels = Object.keys(this.countLoc);
            const values = Object.values(this.countLoc);

            const ctx = document.getElementById("SpotsChart").getContext("2d");

            new Chart(ctx, {
                type: "bar",
                data: {
                    labels,
                    datasets: [
                        {
                            label: "Active Spots Count",
                            data: values,
                            backgroundColor: this.generateColors(values.length),
                            borderColor: "#000",
                            borderWidth: 1,
                            barThickness: 60,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    animation: {
                        duration: 1200,
                        easing: "easeInOutQuart",
                        delay: (context) => this.barAnimationDelay(context),
                    },
                    plugins: { legend: { position: "top" } },
                    scales: { y: { beginAtZero: true } },
                },
            });
        },

        renderDurationChart() {
            if (!this.data.length) return;

            const labels = this.data.map((item) => item.prime_location);
            const durations = this.data.map((item) => item.total_duration);

            const ctx2 = document.getElementById("durationChart2").getContext("2d");

            new Chart(ctx2, {
                type: "bar",
                data: {
                    labels,
                    datasets: [
                        {
                            label: "Total Duration Per Location",
                            data: durations,
                            backgroundColor: this.generateColors(durations.length),
                            borderColor: "#000",
                            borderWidth: 1,
                            barThickness: 60,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    indexAxis: "y",
                    animation: {
                        duration: 1200,
                        easing: "easeInOutQuart",
                        delay: (context) => this.barAnimationDelay(context),
                    },
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
<template>
    <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger', 'text-center']"
        role="alert">
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
<style scoped>
.room-container {
    width: 100%;
    max-width: 900px;
    margin: 4rem auto;
}
</style>

