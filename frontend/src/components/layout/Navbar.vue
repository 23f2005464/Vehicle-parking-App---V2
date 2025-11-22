
<script>
import Button from '@/components/ui/NavButton.vue'

export default {
  name: 'Navbar',

  components: {
    Button
  }
}
</script>


<template>
  
  <nav class="navbar navbar-expand-lg bg-body-tertiary  mx-4">
    <div class="container-fluid">
      <a class="navbar-brand"><img src="@/assets/logo.png" width="50 px" height="30px"></a>
      <p class="navbar-nav ">| PMS Parking Management System</p>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
        </ul>

      </div>
      <div class="nav-Button">
       <router-link to="/login"><Button label="Login"/></router-link> 
      </div>
      <div class="nav-Button">
        <router-link to="/signup"><Button label="Sign Up"/></router-link>
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
}

.container-fluid {
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
  font-size: x-large;
}
.navbar-nav   {
  font-size: large;
  font-weight: 500;
  color: #161d26;
}

@media (max-width: 768px)   {
  .nav-Button {
    margin-left: 0.5rem;
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
  }
  .navbar-nav{
    gap:2rem;
  }
  .container-fluid{
    flex-direction: column;
    align-items: center;
  }
}

</style>
