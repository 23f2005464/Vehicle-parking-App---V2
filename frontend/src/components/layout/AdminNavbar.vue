<script>
import Button from '@/components/ui/NavButton.vue'

export default {
    name: 'UserNavbar',

    components: {
        Button
    },
    user: '',
    methods:{
        logout() {
             localStorage.removeItem("auth_token");
             this.$router.push("/login");
        }
    },
}
</script>


<template>

    <nav class="navbar navbar-expand-lg bg-body-tertiary p-0 m-4 mb-2 cus-nav">
        <div class="container-fluid ">
            <a class="navbar-brand d-flex align-items-center">
                <img src="@/assets/logo.png" width="50" height="30" />
                <span class="ms-2 fw-semibold">| PMS Parking Management System</span>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>


            <div class="collapse navbar-collapse justify-content-start" id="navbarNav">

                <ul class="navbar-nav ">

                    <li class="nav-item">
                        <router-link to="/admin/dashboard" class="nav-link">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/admin/search" class="nav-link">Search</router-link>
                    </li>
                      <li class="nav-item">
                        <router-link to="/admin/userdata" class="nav-link">Users</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/admin/summary" class="nav-link">Summary</router-link>
                    </li>
                    

                    <li class="nav-item">
                        <a @click.prevent="logout" class="nav-link">Logout</a>
                    </li>
                </ul>

            </div>
            <div class="nav-Button">

                <router-link to="/admin/edit_profile"><img src="@/assets/profileicon.png" width="40px" height="40px"
                        style="margin-right: -10px; "></router-link>
            </div>
        </div>
    </nav>
</template>

<style scoped>
.nav-Button {
    margin-left: space-between;
    margin-right: 2rem;
}

.navbar {
    border: solid 0px #161d26;
    border-radius: 40px;
    margin-top: 1rem;
    box-shadow: 0px 3px 10px rgba(11, 112, 92, 0.1);

}

.container-fluid {
    min-width: 100%;
    margin-left: 0.5rem;
    margin-right: 0.5rem;
    padding: 0.5rem;
    padding-left: 3px;
}

.bg-body-tertiary {
    background-color: rgb(226 234 243) !important;
}

.nav-item .nav-link {
    color: #161d26;
    font-weight: 500;
    transition: 0.5s;
    font-size: larger;
    margin-left: 1.5rem;
}

.navbar-nav {
    font-size: large;
    font-weight: 500;
    color: #161d26;
    justify-items: flex-start;
    gap: 5rem;
}
.nav-item .nav-link:hover {
   font-weight: bolder;
    transition: 0.5s;
    color: rgb(0, 0, 0);
}

.cus-nav {
    padding: 0px !important;
}

@media (max-width: 976px) {
    .nav-Button {
        margin-left: 0.5rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .navbar-nav {
        gap: 2rem;
    }

    .container-fluid {
        flex-direction: column;
        align-items: center;
    }

}
</style>
