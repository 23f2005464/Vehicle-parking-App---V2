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
        admin_download_csv() {
            console.log("Admin Download requested");

            const token = localStorage.getItem("auth_token");

            fetch("http://127.0.0.1:5000/api/celery/admin/download_all_reservations", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Token-Auth": token
                }
            })
                .then(res => res.json())
                .then(start => {
                    const taskId = start.task_id;
                    console.log("Admin CSV task started:", taskId);

                    const interval = setInterval(() => {

                        fetch("http://127.0.0.1:5000/api/celery/admin/user_get_data/" + taskId, {
                            method: "GET",
                            headers: {
                                "Content-Type": "application/json",
                                "Token-Auth": token
                            }
                        })
                            .then(res => res.json())
                            .then(status => {
                                console.log("Admin Status:", status);

                                if (status.status === "pending") return;

                                clearInterval(interval);

                        
                                if (status.status === "error") {
                                    console.error("Admin CSV generation failed:", status.message);
                                    return;
                                }

                   
                                if (status.status === "ready") {
                                    const url =
                                        "http://127.0.0.1:5000/api/celery/admin_user_download_csv?token=" +
                                        status.token;

                                    console.log("Admin Downloading:", url);

                                    // Window download method
                                    window.open(url, "_blank");
                                }
                            })
                            .catch(err => {
                                clearInterval(interval);
                                console.error("Admin polling failed:", err);
                            });

                    }, 500);
                })
                .catch(err => {
                    console.error("Admin task creation failed:", err);
                });
        }
        ,
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
    <div class="container">
        <h4>Download All Users Parked Data </h4>
        <Button @click="admin_download_csv" label="Download" height="50px" radius="15px">
        </Button>
    </div>
</template>
<style scoped>
.text-center {
    text-align: center;
}
.container{
    display: flex;
    gap:1.6rem;
    justify-content: center;
    margin-top: 3rem;
    align-items: center;
    
}
.container h4{
    font-weight: bold;
}
</style>