<script>
import Button from '@/components/ui/NavButton.vue'

export default {
    name: 'ProfilePage',
    components: { Button },

    data() {
        return {
            userData: {},
            message: '',
            messageType:'',
            editMode: false,
            formData: { // corrected case
                fullname: '',
                address: '',
                pincode: ''
            }
        }
    },

    mounted() {
        fetch(`${this.$apiBase}/api/auth/profile`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Token-Auth': localStorage.getItem('auth_token')
            },
        })
            .then(res => res.json())
            .then(data => {
                this.userData = data;
                this.formData.fullname = data.fullname;
                this.formData.address = data.address;
                this.formData.pincode = data.pincode;
            })
            .catch(err => console.error(err));
    },


    methods: {
        toggleEdit() {
            this.editMode = !this.editMode;
        },

        saveProfile() {
            fetch(`${this.$apiBase}/api/admin/update_profile`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Token-Auth': localStorage.getItem('auth_token')
                },
                body: JSON.stringify({
                    fullname: this.formData.fullname,
                    address: this.formData.address,
                    pincode: this.formData.pincode
                })
            })
                .then(res => res.json())
                .then(data => {
                    this.message = data.message;
                    this.messageType = "success";
                    this.editMode = false;
                    //for instant update without refresh
                    this.userData.fullname = this.formData.fullname;
                    this.userData.address = this.formData.address;
                    this.userData.pincode = this.formData.pincode;
                    setTimeout(() => {
                        this.message = '';
                         this.$router.push("/admin/edit_profile");
                    }, 3000);
                   
                })
                .catch(err => console.error(err));
        }
    }
}
</script>

<template>
   <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger','text-center'] " role="alert">
  {{ message }}
</div>

    
     <div class="payment-container">    
        <h1 class="page-title">Profile</h1>

        <div v-if="userData">

            <div class="mb-3 row">
                <label class="col-sm-4 label-text">User ID:</label>
                <div class="col-sm-8">
                    <div class="value-box">{{ userData.user_id }}</div>
                </div>
            </div>

            <div class="mb-3 row">
                <label class="col-sm-4 label-text">Email ID:</label>
                <div class="col-sm-8">
                    <div class="value-box">{{ userData.email }}</div>
                </div>
            </div>

            <!-- Name -->
            <div class="mb-3 row">
                <label class="col-sm-4 label-text">Name:</label>
                <div class="col-sm-8">
                    <div v-if="!editMode" class="value-box">{{ userData.fullname }}</div>
                    <input v-else v-model="formData.fullname" class="form-control" />
                </div>
            </div>

            <!-- Address -->
            <div class="mb-3 row">
                <label class="col-sm-4 label-text">Address:</label>
                <div class="col-sm-8">
                    <div v-if="!editMode" class="value-box">{{ userData.address }}</div>
                    <input v-else v-model="formData.address" class="form-control" />
                </div>
            </div>

            <!-- Pincode -->
            <div class="mb-3 row">
                <label class="col-sm-4 label-text">Pincode:</label>
                <div class="col-sm-8">
                    <div v-if="!editMode" class="value-box">{{ userData.pincode }}</div>
                    <input v-else v-model="formData.pincode" class="form-control" />
                </div>
            </div>

            <div class="btn-group-custom">
                <Button v-if="!editMode" @click="toggleEdit" label="Edit" radius="10px" />
                <Button v-else @click="saveProfile" label="Save" radius="10px" />
                <Button v-if="editMode" @click="toggleEdit" label="Cancel" radius="10px" />
                <router-link to="/admin/dashboard">
                    <Button label="Back" radius="10px" />
                </router-link>
            </div>

        </div>

        <div v-else>
            <p class="text-center">Fetching profile details...</p>
        </div>

    </div>
</template>

<style scoped>
.payment-container {
    max-width: 700px;
    margin: 40px auto;
    padding: 30px;
    background: #fff;
    border-radius: 12px;
    border: 2px solid black;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2);
}

.page-title {
    text-align: center;
    margin-bottom: 30px;
    font-weight: 700;
}

.label-text {
    font-weight: 600;
}

.value-box {
    background-color: #f5f5f5;
    padding: 10px 12px;
    border-radius: 6px;
    border: 1px solid #aaa;
    width: 100%;
}

.form-control {
    width: 100%;
    padding: 8px;
    border-radius: 6px;
    border: 1px solid #aaa;
}

.btn-group-custom {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 25px;
}

.alert {
    width: 60%;
    margin: 10px auto;
    text-align: center;
    padding: 10px;
    border-radius: 6px;
}

.alert-success {
    background: #d4edda;
    color: #155724;
}
</style>

