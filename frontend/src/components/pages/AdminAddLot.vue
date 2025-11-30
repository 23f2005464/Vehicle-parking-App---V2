<script>
import Button from '@/components/ui/NavButton.vue'
export default {
    name: 'AdminAddLot',
    components: {
        Button
    },
    data() {
        return {
            FormData: {
                prime_location: '',
                address: '',
                pincode: '',
                max_no_of_spots: '',
                price_per_hour_of_spot: ''
            },
            message: '',
            messageType: '',
            loading: false,
        }
    },
    methods: {
        Add_lot() {
            if (this.loading) return;
            this.loading = true;
            fetch('http://127.0.0.1:5000/api/admin/create_lot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Token-Auth': localStorage.getItem('auth_token')
                },
                body: JSON.stringify({
                    "prime_location": this.FormData.prime_location,
                    "price_per_hour": this.FormData.price_per_hour_of_spot,
                    "total_spaces": this.FormData.max_no_of_spots,
                    "pincode": this.FormData.pincode,
                    "address": this.FormData.address
                })
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Preview Data:', data);
                    if (data.message) {
                        this.message = data.message;
                        this.messageType = 'success'
                        setTimeout(() => {
                            this.message = '';
                            this.$router.push("/admin/dashboard")
                        }, 1000)

                    } else {
                        this.messageType = "error"
                        console.error('Error in creating lot', data.message);
                    }
                })
                .catch(err => console.error('Error', err))
                .finally(() => {
                    this.loading = false; // re-enable button
                });
        }
    }

}
</script>
<template>
    <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger', 'text-center']"
        role="alert">
        {{ message }}
    </div>
    <div class="container mt-5 p-4 border rounded ">

        <h1 class="page-title">Add Lot</h1>

        <div class="mb-3 row ms-4">
            <label class="col-sm-2 label-text">Prime location:</label>
            <div class="col-sm-9">
                <input class="value-box" placeholder="location"  type="text"  v-model="FormData.prime_location"></input>
            </div>
        </div>

        <div class="mb-3 row  ms-4">
            <label class="col-sm-2 label-text">Address:</label>
            <div class="col-sm-9">
                <input class="value-box" placeholder="Address of lot" type="text"  v-model="FormData.address"></input>
            </div>
        </div>

        <div class="mb-3 row  ms-4">
            <label class="col-sm-2 label-text">Pincode:</label>
            <div class="col-sm-9">
                <input class="value-box" type="text"   placeholder="Pincode of lot" v-model="FormData.pincode"></input>
            </div>
        </div>

        <div class="mb-3 row  ms-4">
            <label class="col-sm-2 label-text">Spots:</label>
            <div class="col-sm-9">
                <input class="value-box"  type="number"   placeholder="No. of spots Max" v-model.number="FormData.max_no_of_spots"></input>
            </div>
        </div>

        <div class="mb-3 row  ms-4">
            <label class="col-sm-2 label-text">Price(per hour):</label>
            <div class="col-sm-9">
                <input class="value-box" type="number" placeholder="price per hour of spot"
                    v-model.number="FormData.price_per_hour_of_spot"></input>
            </div>
        </div>



        <div class="btn-group-custom">
            <Button @click="Add_lot" :disabled="loading" label="Add" radius="10px" padding="15px 25px"
                fs="20px" height="60px"></Button>
            <a><router-link to="/admin/dashboard"><Button label="Cancel" radius="10px" padding="15px 25px"
                        fs="20px" height="60px" ></Button></router-link></a>
        </div>
    </div>
</template>

<style scoped>
.container {
    max-width: 1000px;

}

.btn-group-custom {
    display: flex;
    flex-direction: row;
    justify-content: center;
}
</style>