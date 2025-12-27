<script>
import Button from '@/components/ui/NavButton.vue'

const SEARCH_MAP = {
    "Parking Lots": {
        "pincode": { url: `${this.$apiBase}/api/admin/search/lot`, key: "pincode" },
        "lot id": { url: `${this.$apiBase}/api/admin/search/lot`, key: "lot_id" },
        "name": { url: `${this.$apiBase}/api/admin/search/lot`, key: "prime_location" }
    },
    "Parking Spots": {
        "spot id": { url: `${this.$apiBase}/api/admin/search/spot`, key: "spot_id" },
        "lot id": { url: `${this.$apiBase}/api/admin/search/spot`, key: "lot_id" }
    },
    "User": {
        "user id": { url: `${this.$apiBase}/api/admin/search/user`, key: "user_id" },
        "user name": { url: `${this.$apiBase}/api/admin/search/user`, key: "name" },
        "email": { url: `${this.$apiBase}/api/admin/search/user`, key: "email" },
    }
};

export default {
    name: "SearchPage",
    components: {
        Button: Button
    },
    data() {
        return {
            query: '',
            selectedOption: 'Parking Lots',
            selectedOptiontype: 'pincode',
            SearchedResult: [],
            InfoUserResult: [],
            SearchedResultflag: false,
            message: '',
            messageType: '',
            Popup: false,

        }
    },
    methods: {
        formatTime(timeString) {
            const d = new Date(timeString);
            const ist = new Date(d.getTime() + (5.5 * 60 * 60 * 1000));

            return ist.toISOString().slice(0, 19).replace("T", " ");
        },
        
        storeSelection() {
            if (this.selectedOption === 'User') {
                this.selectedOptiontype = 'user id';
            }
            else if (this.selectedOption === 'Parking Spots') {
                this.selectedOptiontype = 'spot id';
            }
            else {
                this.selectedOptiontype = 'pincode';
            }
        },
        api(url, payload) {
            return fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Token-Auth": localStorage.getItem("auth_token")
                },
                body: JSON.stringify(payload)
            })
                .then(res => res.json().then(data => ({ status: res.status, data: data })));
        }
        ,
        handleApiResult(result) {
            if (result.status === 404) {
                this.message = result.data.message || "No results found.";
                this.messageType = "error";
                this.SearchedResult = [];
                this.SearchedResultflag = false;

                setTimeout(() => {
                    this.message = "";
                }, 2000);

                return false;
            }

            return true;
        },

        storeTypeSelection() { },
        handleSearch() {

            if (this.selectedOptiontype === "pincode" && this.query.length < 6) {
                this.message = "Please enter valid pincode";
                this.messageType = "error";
                setTimeout(() => { this.message = ""; }, 2000);
                return;
            }

            const config = SEARCH_MAP[this.selectedOption][this.selectedOptiontype];

            if (!config) return;

            const payload = {
                [config.key]: this.query
            };

            this.api(config.url, payload)
                .then(result => {

                    if (!this.handleApiResult(result)) return; //if return 404 stop further execution

                    this.SearchedResult = result.data;
                    this.SearchedResultflag = true;
                });
        }
        ,
        ReservationInfo(user_id) {
            fetch("http://127.0.0.1:5000/api/admin/search/view_user_res_info", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Token-Auth': localStorage.getItem('auth_token')
                },
                body: JSON.stringify({
                    "user_id": user_id
                })

            })
                .then(res => res.json().then(data => ({ status: res.status, data: data })))

                .then(result => {
                    if (result.status === 404) {
                        this.message = result.data.message || "No reservation found.";
                        this.messageType = "error";
                        setTimeout(() => {
                            this.message = '';
                        }, 2000);
                        return;
                    }
                    this.Popup = true;
                    this.InfoUserResult = result.data;
                    this.SearchedResultflag = true;

                    console.log(this.SearchedResult);
                })

        }
    }

};


</script>


<template>
    <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger', 'text-center']"
        role="alert">
        {{ message }}
    </div>
    <div class="container">
        <h2 class="m-4 search-head">
            <label class="label">Search Category:</label>
            <select v-model="selectedOption" class="form-select mt-4" @change="storeSelection">
                <option value="Parking Lots">Parking Lots</option>
                <option value="Parking Spots">Parking Spots</option>
                <option value="User">Users</option>
            </select>
            <label class="label mt-3">Search By: </label>
            <select v-if="selectedOption === 'User'" v-model="selectedOptiontype" class="form-select mt-4"
                @change="storeTypeSelection">
                <option value="user id">User Id</option>
                <option value="user name">Name</option>
                <option value="email">Email</option>
            </select>


            <select v-else-if="selectedOption === 'Parking Spots'" v-model="selectedOptiontype" class="form-select mt-4"
                @change="storeTypeSelection">
                <option value="spot id">Spot Id</option>
                <option value="lot id">Lot Id</option>
            </select>

            <select v-else v-model="selectedOptiontype" class="form-select mt-4" @change="storeTypeSelection">
                <option value="pincode">Pincode</option>
                <option value="name">Prime Location</option>
                <option value="lot id">Lot Id</option>
            </select>
            <div v-if="selectedOption === 'Parking Lots' && selectedOptiontype === 'pincode'"
                class="d-flex justify-content-center mt-3">
                <input v-model="query" class="form-control me-2 mt-3 custom-input" type="text"
                    :placeholder="selectedOptiontype" maxlength="6" />
                <Button label="Search" class="mt-3 " radius="10px" height="53px" @click="handleSearch()" />
            </div>


            <div v-else class="d-flex justify-content-center mt-3">
                <input v-model="query" class="form-control me-2 mt-3 custom-input" type="text"
                    :placeholder="selectedOptiontype" />
                <Button label="Search" class="mt-3 " radius="10px" height="53px" @click="handleSearch()" />
            </div>


            <div class="container d-flex   mt-4" v-if="selectedOption === 'Parking Lots'">
                <div v-if="SearchedResultflag" v-for="(lot, index) in SearchedResult" :key="index" class="card mt-4">
                    <h5><b>{{ lot.prime_location }}</b>
                    </h5>
                    <p><strong>Lot id:</strong> {{ lot.lot_id }}</p>
                    <p><strong>Pincode:</strong> {{ lot.pincode }}</p>
                    <p><strong>Available Spots:</strong> {{ lot.available_spots }} / {{ lot.total_spaces }}</p>
                    <p><strong>Occupied spots:</strong> {{ lot.total_spaces - lot.available_spots }}</p>
                    <p><strong>Price per hour:</strong> {{ lot.price_per_hour_of_spot }}</p>
                    <div class="d-flex  gap-3 justify-content-between mt-2">
                        <router-link :to="{ name: 'AdminEditLot', params: { lot_id: lot.lot_id } }"><Button
                                label=" Edit" radius="10px" bgcolor="#F97316" hoverColor=" #EA580C" /></router-link>
                        <router-link :to="{ name: 'AdminSpotsPage', params: { lot_id: lot.lot_id } }"><Button
                                label="Spots" radius="10px" hoverColor="#4338CA" bgcolor="#4F46E5" /></router-link>
                    </div>
                </div>




            </div>
            <div class="container  d-flex" v-else-if="selectedOption === 'Parking Spots'">
                <div v-if="SearchedResultflag" v-for="(spot, index) in SearchedResult" :key="index"
                    class="card spot-card mt-4">
                    <h6><b>Spot ID: {{ spot.spot_id }}</b>
                    </h6>
                    <p><b>Lot id:</b> {{ spot.lot_id }}</p>
                    <p><b>Status:</b></p>

                    <span :class="{ redspot: spot.status === 'R', greenspot: spot.status !== 'R' }">{{ spot.status ==='R'?'Reserved' : 'Available' }}</span>
                    
                </div>

            </div>
            <div class="container  d-flex" v-else-if="selectedOption === 'User'">
                <div v-if="SearchedResultflag && Popup === false" v-for="(user, index) in SearchedResult" :key="index"
                    class="card mt-4">
                    <h5><b>{{ user.fullname }}</b>
                    </h5>
                    <p><strong>User id:</strong> {{ user.user_id }}</p>
                    <p><strong>Email:</strong> {{ user.email }}</p>
                    <p><strong>Address:</strong> {{ user.address }}</p>
                    <p><strong>Pincode:</strong> {{ user.pincode }}</p>
                    <p><strong>Reservations:</strong>{{ user.reservations }}</p>
                    <Button label="info" radius="10px" height="40px" @click="ReservationInfo(user.user_id)" />
                </div>

            </div>


        </h2>
        <div v-if="Popup" class="popup-overlay" @click.self="Popup = false">

            <div class="popup-card">
                <h2 class="popup-title">Reservation Information</h2>

                <div v-for="(res, index) in InfoUserResult" :key="index" class="card mb-3 popup-cards">
                    <p><b>Reservation ID:</b> {{ res.reservation_id }}</p>
                    <p><b>Spot ID:</b> {{ res.spot_id }}</p>
                    <p><b>Lot ID:</b> {{ res.lot_id }}</p>
                    <p><b>Parking Time:</b> {{ formatTime(res.parking_start) }}</p>
                    <p><b>Duration (hrs):</b> {{ res.duration }}</p>
                    <p><b>Amount to Pay:</b> ₹{{ res.amount }}</p>
                    <p><b>Vehicle Number:</b> {{ res.vehicle_number }}</p>
                </div>

                <button class="close-btn" @click="Popup = false">Close</button>
            </div>
        </div>

    </div>
</template>
<style scoped>
.search-head ul li {
    display: inline-block;
}

.container {
    gap: 1rem;
    flex-wrap: wrap;
    overflow-y: auto;
}

select {
    background-color: #f8f8f8;
    border: 1px solid #777;
    padding: 10px;
    border-radius: 30px;
}

.form-select:focus {
    border-color: aliceblue !important;
    box-shadow: 0px 0px 20px rgba(5, 164, 179, 0.5) !important;
}

.label {
    font-weight: bold;
    font-size: 18px;
    margin-right: 10px;
}

.form-control {
    line-height: 2.5rem;
}

.form-control:focus {
    border-color: aliceblue !important;
    box-shadow: 0px 0px 20px rgba(5, 164, 179, 0.5) !important;
}

.card {
    min-width: fit-content;
    padding: 1rem;
    text-align: justify;
    transition: all 0.3s ease;
    display: inline-block;
    background-color: rgb(159, 243, 237);

}

.card:hover {
    box-shadow: 0 10px 20px rgba(24, 221, 239, 0.5);
    transform: translateY(-5px);
}

.card h5 {
    margin-bottom: 18px !important;
    text-align: center;
    font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    font-size: x-large;

}

.card p {
    margin-bottom: 0.5rem !important;
    line-height: 1.3 !important;
    font-size: 15px;
}

.spot-card {
    min-width: 200px;
    padding: 1rem;
    text-align: justify;
    transition: all 0.3s ease;
    display: inline-block;
    background-color: rgb(159, 243, 237);
}

.redspot {
    color: red;
    font-weight: bold;
}

.greenspot {
    color: green;
    font-weight: bold;
}

.popup-overlay {
    position: fixed;
    left: 0;
    top: 0;

    width: 100%;
    height: 100%;
    backdrop-filter: blur(4px);
    /* ★ BLUR EFFECT */
    background: rgba(0, 0, 0, 0.4);
    /* slight dark */
    display: flex;
    align-items: center;
    justify-content:center;

    z-index: 999;
}

.popup-card {
    width: 50%;
    max-height: 600px;
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
    gap: 1rem;
    justify-content:flex-start;
    align-items: center;
    overflow-y: scroll;

}

.popup-card::-webkit-scrollbar {
    display: none;
}

.popup-card:hover {
    box-shadow: 0px 10px 20px rgba(124, 228, 238, 0.5);
    opacity: 30px;
}

.popup-cards {
    background-color: rgb(42, 183, 150);
    width: 90%;
}

.popup-title {
    margin-bottom: 15px;
    text-align: center;
    font-weight: 700;
}

</style>
