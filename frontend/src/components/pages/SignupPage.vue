<script >
import { API_BASE } from "@/api";
export default {
  name: 'SignupPage',
  data(){
    return {
        email:'',
        password:'',
        fullname:'',
        address:'',
        pincode:''
    }
  }, 
  methods:{
    signupuser(){
        if (!this.email||!this.password||!this.fullname||!this.address||!this.pincode){
            alert("please fill all creditionals")
            return
        }
        console.log("User is :",this.email,this.fullname)
        fetch(`${API_BASE}/api/auth/register`,{
            method : 'POST',
            headers :  {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'email':this.email,
            'password':this.password,
            'fullname':this.fullname,
            'pincode':this.pincode,
            'address':this.address
        })})
        
        .then(response=> response.json())
        .then(data => {
             alert(data.message)
             this.$router.push('/login')
        })
         .catch(error => {
          console.error('Error during login:', error)
          alert("An error occurred during login.")

        })
    }

  }
}

</script>

<template>
  <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger','text-center'] " role="alert">
  {{ message }}
</div>

<div class="brand-logo">
    <img src="@/assets/logo.png" width="80px" height="50px" class="d-block mx-auto" />
    <h1 class="text-center my-4">PMS Parking Management System</h1>
  </div>

  <div class="custom-body">
    <div class="login-container text-center">
      <h2 class="mb-4">Register </h2>

      <div class="mb-3 text-start">
        <label for="email" class="form-label">Email address</label>
        <input type="text" class="form-control" id="email" placeholder="Enter email" v-model="email" />
      </div>

      <div class="mb-3 text-start">
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" id="password" placeholder="Password" v-model="password" />
      </div>
    <div class="mb-3 text-start">
        <label for="fullname" class="form-label">Full Name</label>
        <input type="text" class="form-control" id="fullname" placeholder="Name Middle Surname" v-model="fullname" />
      </div>
      <div class="mb-3 text-start">
        <label for="address" class="form-label">Address</label>
        <input type="text" class="form-control" id="address" placeholder="Enter address" v-model="address" />
      </div>
<div class="mb-3 text-start">
        <label for="pincode" class="form-label">Pincode</label>
        <input type="text" class="form-control" id="pincode" placeholder="Enter pincode" v-model="pincode" />
      </div>


      
      <button @click="signupuser" class="btn btn-primary w-100">Sign up</button>
    </div>
  </div>
</template>

<style scoped>
.brand-logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 5%;
}
.custom-body {
  display: flex;
  align-items: center;
  justify-content: center;
}
.login-container {
  background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
    url('@/assets/v859-katie-11.jpg');
  border: 1px solid #767575;
  border-radius: 10px;
  padding: 2rem;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
  color: #fff;
}
.form-control {
  background-color: #9e9999b9;
  border: 1px solid #444;
  color: #fff;
}
.form-control:focus {
  background-color: #000;
  border-color: #888;
  box-shadow: none;
}
.btn-primary {
  background-color: #1f2424;
  color: #ffffff;
  border: none;
}
.btn-primary:hover {
  background-color: #00bcd4;
  color: #000000;
  font-weight: 650;
}
a {
  color: #bbb;
  text-decoration: none;
}
a:hover {
  color: #fff;
  text-decoration: underline;
}
</style>

