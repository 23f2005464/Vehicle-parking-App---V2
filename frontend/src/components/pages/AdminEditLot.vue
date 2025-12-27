<script>
import Button from '@/components/ui/NavButton.vue'

export default {
    name: "AdminEditLot",
    components: { Button },

    data() {
        return {
            message: "",
            message_Type: "",
            FormData: {
                lot_id: "",
                prime_location: "",
                address: "",
                pincode: "",
                available_spots: "",
                total_spaces: "",
                price_per_hour_of_spot: ""
            },
            originalData: {}
        }
    },

    methods: {
        View_lot() {
            const lot_id = this.$route.params.lot_id;

            fetch(`${this.$apiBase}/api/admin/view_lot`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Token-Auth": localStorage.getItem("auth_token"),
                },
                body: JSON.stringify({ lot_id }),
            })
                .then(res => res.json())
                .then(data => {
                    if (data) {
                        this.FormData = { ...data }
                        this.originalData = { ...data }
                    } else {
                        this.message_type = "error";
                        this.message = data.message || "Failed to load lot";
                    }
                })
                .catch(err => console.error("Error:", err));
        },
        Edit_lot() {
            // Create an object with only the edited fields
            const editedData = {};

            for (const key in this.FormData) {
                if (this.FormData[key] !== this.originalData[key]) {
                    editedData[key] = this.FormData[key];
                }
            }

            // Always include lot_id
            editedData.lot_id = this.FormData.lot_id;

            fetch(`${this.$apiBase}/api/admin/edit_lot`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Token-Auth": localStorage.getItem("auth_token"),
                },
                body: JSON.stringify(editedData),
            })
                .then(res => res.json())
                .then(data => {
                    if (data.message) {
                        if(data.message==="Not enough available spots to remove"){

                            throw new Error(data.message);
                        }else {
                        this.messageType = "success";
                        this.message = data.message;
                    
                        this.originalData = { ...this.FormData };
                        setTimeout(()=> {
                            this.message='',
                            this.$router.push('/admin/dashboard')
                        },2000
                    )
                    }} else {
                          throw new Error(data.message);
                    }
                })
                .catch(err => {
                    this.message_type = "error";
                    this.message =  err.message;
                });
        }
        ,      
    },
    mounted() {
            this.View_lot();
        }
}
</script>



<template>
 <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger','text-center'] " role="alert">
  {{ message }}
</div>

    <div class="container mt-5 p-4 border rounded">

        <h1 class="page-title">Edit Lot</h1>

        <div class="mb-3 row ms-4">
            <label class="col-sm-2">Prime location:</label>
            <div class="col-sm-9">
                <input class="value-box" v-model="FormData.prime_location" />
            </div>
        </div>

        <div class="mb-3 row ms-4">
            <label class="col-sm-2">Address:</label>
            <div class="col-sm-9">
                <input class="value-box" v-model="FormData.address" />
            </div>
        </div>

        <div class="mb-3 row ms-4">
            <label class="col-sm-2">Pincode:</label>
            <div class="col-sm-9">
                <input class="value-box" v-model="FormData.pincode" />
            </div>
        </div>

        <div class="mb-3 row ms-4">
            <label class="col-sm-2">Spots:</label>
            <div class="col-sm-9">
                <input class="value-box" v-model="FormData.total_spaces" />
            </div>
        </div>

        <div class="mb-3 row ms-4">
            <label class="col-sm-2">Price (per hour):</label>
            <div class="col-sm-9">
                <input class="value-box" v-model="FormData.price_per_hour_of_spot" />
            </div>
        </div>

        <div class="btn-group-custom">
            <Button label="Save" @click="Edit_lot" radius="10px" padding="15px 25px" fs="20px" height="60px"/>
            <router-link to="/admin/dashboard">
                <Button label="Cancel" radius="10px" padding="15px 25px" fs="20px" height="60px" />
            </router-link>
        </div>
    </div>
</template>



<style scoped>
.container {
    max-width: 1000px;
}

.btn-group-custom {
    display: flex;
    justify-content: center;
}
</style>


