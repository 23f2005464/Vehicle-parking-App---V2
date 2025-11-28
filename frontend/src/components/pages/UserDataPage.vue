<script>
import Button from '@/components/ui/NavButton.vue';
export default {
    name: "UserDataPage",
    components: {
        Button

    },
    data() {
        return {
            users: [],
            userBanned: false,
            message: '',
            messageType: ''
        };
    },
    methods: {
        fetchUserData() {
            fetch("http://127.0.0.1:5000/api/admin/view_users", {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Token-Auth': localStorage.getItem('auth_token')
                }
            })

                .then((response) => response.json())
                .then((data) => {
                    this.users = data;
                    console.log("Fetched user data:", data);
                })
                .catch((error) => {
                    console.error("Error fetching user data:", error);
                });
        }
        ,
        UnBanUser(user_id) {
            fetch(`http://127.0.0.1:5000/api/admin/unban_user`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Token-Auth': localStorage.getItem('auth_token')
                },
                body: JSON.stringify({ user_id: user_id })
            })
                .then(res => res.json())
                .then(data => {
                    console.log('User unbanned successfully:', data);
                    this.message = "User unbanned successfully";
                    this.messageType = "success";
                    this.userBanned = false;
                    setTimeout(() => {
                        this.message = '';
                    }, 2000);
                    this.fetchUserData(); // Refresh the user list after unbanning
                })
        },
        BanUser(user_id) {
            fetch(`http://127.0.0.1:5000/api/admin/ban_user`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Token-Auth': localStorage.getItem('auth_token')
                },
                body: JSON.stringify({ user_id: user_id })
            })
                .then(res => res.json())
                .then(data => {
                    console.log('User banned successfully:', data);
                    this.message = "User banned successfully";
                    this.messageType = "success";
                    this.userBanned = true;
                    setTimeout(() => {
                        this.message = '';
                    }, 2000);
                    this.fetchUserData(); // Refresh the user list after banning
                })
        },
    },

    mounted() {
        this.fetchUserData();
    }

}

</script>
<template>
    <div class="text-center mt-4">
        <h2>User Data</h2>
        <table class="table table-striped mx-auto" style="width: 90%;">
            <thead>
                <tr>
                    <th>User ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Pincode</th>
                    <th>Active</th>
                    <th>Action</th>
                </tr>

            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.id">
                    <td>{{ user.user_id }}</td>
                    <td>{{ user.fullname }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.pincode }}</td>
                    <td>{{ user.active }}</td>
                    <Button v-if="user.active === true" label="Ban" bgcolor="#000000" radius="10px" hover-color="Red"
                        @click="BanUser(user.user_id)" />
                    <Button v-if="user.active === false" label="UnBan" bgcolor="#1055C9" radius="10px"
                        hover-color="08CB00" @click="UnBanUser(user.user_id)" />

                </tr>

            </tbody>
        </table>
    </div>
</template>
<style scoped>
.text-center {
    text-align: center;
}
</style>