<script>
import Button from '@/components/ui/NavButton.vue'
export default {
    name: "AdminSpotsPage",
    components: {
        Button
    },
    data() {
        return {
            data_spots: [],
            SelectedSpot: null,
            ShowDel: false,
            message: '',
            messageType: '',
            lot_id: '',
            user_data: [],
            showUserPopup: false
        }
    },
    methods: {
        SelectSpot(spot_id) {
            const spot = this.data_spots.spots.find(s => s.spot_id === spot_id)
            if (spot.status === 'R') {
                this.ShowDel = false
                this.SelectedSpot = spot_id
            }
            else {
                this.SelectedSpot = spot_id
                this.ShowDel = true
            }
        },
        DelSpot(spot_id) {
            if (!confirm(`Are you sure you want to delete spot ${spot_id}?`)) {
                return;   
            } 
            fetch("http://127.0.0.1:5000/api/admin/delete_spot", {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Token-Auth': localStorage.getItem('auth_token')
                },
                body: JSON.stringify({
                    "spot_id": spot_id
                })
            })
                .then(res => res.json())
                .then(data => {
                    if (data.message === "Spot deleted successfully") {
                        this.data_spots.spots = this.data_spots.spots.filter(x => x.spot_id !== spot_id)  //return list of spots that is exclude spot_id
                        this.message = data.message;
                        this.messageType = "success";
                        this.SelectedSpot = null;
                        this.ShowDel = false;
                        setTimeout(() => {
                            this.message = '';
                        }, 1000)
                    }
                    else {
                        this.messageType = "error"
                        this.message = data.message
                    }
                })
                .catch(err => {
                    this.messageType = 'error'
                    this.message = err.message
                })

        },
        Userdata(spot_id) {
            fetch(`${this.$apiBase}/api/admin/view_spot`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Token-Auth': localStorage.getItem('auth_token')
                },
                body: JSON.stringify({
                    "spot_id": spot_id
                })
            })
                .then(res => res.json())
                .then(data => { this.user_data = data; this.showUserPopup = true; })
        }
    },

    mounted() {
        this.lot_id = this.$route.params.lot_id
        fetch(`${this.$apiBase}/api/admin/view_spots`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Token-Auth': localStorage.getItem('auth_token')
            },
            body: JSON.stringify({
                "lot_id": this.lot_id
            })
        })
            .then(res => res.json())
            .then(data => this.data_spots = data)

    }
}
</script>

<template>


    <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger', 'text-center']"
        role="alert">
        {{ message }}
    </div>
    <h1 class="text-center mb-2 mt-4 fw-semibold fs-2">Parking lots</h1>


    <div class="container border rounded" style="background-color: #f5f5f5;">

        <div class="con" v-for="(spot, index) in data_spots.spots" :key="spot.spot_id">

            <div class="small-square" :class="{redSpot: spot.status === 'R', selected: SelectedSpot === spot.spot_id}" @click="SelectSpot(spot.spot_id)">
                <span v-if="ShowDel === true && SelectedSpot === spot.spot_id">
                    <img src="@\assets\delete.png" class="del-icon" @click="DelSpot(spot.spot_id)">
                </span>

                <h1 v-if="!(SelectedSpot === spot.spot_id)">{{ index + 1 }}</h1>

                <div v-if="spot.status === 'R' && SelectedSpot === spot.spot_id">
                    <img src="@/assets/image.png" width="40px" @click="Userdata(spot.spot_id)">
                </div>
            </div>
            <h6 style="margin-top: 15px;">#spot id: <b>{{ spot.spot_id }}</b></h6>
        </div>
    </div>
    <div v-if="showUserPopup" class="popup-overlay" @click.self="showUserPopup = false">

        <div class="popup-card">
            <h2 class="popup-title">Reserved By</h2>

            <p><b>Name:</b> {{ user_data.name }}</p>
            <p><b>Email:</b> {{ user_data.email }}</p>
            <p><b>Vehicle No:</b> {{ user_data.vehicle_number }}</p>
            <p><b>Parking Time:</b> {{ user_data.parking_timestamp }}</p>

            <button class="close-btn" @click="showUserPopup = false">Close</button>
        </div>

    </div>

</template>

<style scoped>
.container {
    min-height: 600px;
    max-height: 600px;
    overflow-y: scroll;
    display: flex;
    flex-wrap: wrap;
    column-gap: 15px;
    /* gap left-right */
    row-gap: 20px;
    align-content: flex-start;
    justify-content: center;


}

.container::-webkit-scrollbar {
    display: none;
}

/* When spot.status = "R" */
.redSpot {
    background-color: red !important;
    border-color: darkred !important;
    color: white;
}

.small-square.redSpot:hover {
    transform: scale(0.9);
    cursor: pointer;
    box-shadow: 0 10px 20px rgb(235, 0, 0);
}

.con {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.small-square {
    margin-top: 1rem;
    width: 5rem;
    height: 5rem;
    background-color: #14e71e;
    ;
    border: solid;
    border-radius: 15px;
    border-width: 3px;
    display: flex;
    align-items: center;
    justify-content: center;

    transition: background-color 0.3s ease, border-color 0.3s ease, transform 0.2s ease;
}

.small-square h1 {
    transform: scale(0.8);


}

.small-square:hover {
    transform: scale(0.9);
    cursor: pointer;
    box-shadow: 0 10px 20px rgb(64, 255, 0);

}

.small-square.selected {
    outline: 3px solid rgb(255, 0, 0);
    /* highlight selected spot */
    background-color: #ffe6e6 !important;
    box-shadow: 0 2px 8px rgb(0, 0, 0);
    transform: matrix(1, 2, 3);
}

.del-icon {
    width: 40px;
    cursor: pointer;
}



/* Background blur overlay */
.popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    backdrop-filter: blur(5px);
    /* ★ BLUR EFFECT */
    background: rgba(0, 0, 0, 0.4);
    /* slight dark */
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999;
}

/* Popup rectangle card */
.popup-card {
    width: 350px;
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.3);
    animation: popupFade 0.3s ease-out;
}

.popup-card:hover {
    box-shadow: 0px 10px 20px rgba(24, 221, 239, 0.5);
    opacity: 30px;
}

.popup-title {
    margin-bottom: 15px;
    text-align: center;
    font-weight: 700;
}

@keyframes popupFade {
    from {
        transform: translateY(-50px);
        opacity: 0;
    }

    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.close-btn {
    margin-top: 15px;
    width: 100%;
    padding: 10px;
    background: #ff4d4d;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

.close-btn:hover {
    background: #e60000;
}

</style>
