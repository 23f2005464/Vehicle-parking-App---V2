<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      FormData: {
        email: '',
        password: '',
      },
      message: '',
      messageType: ''
    }


  },
  methods: {
    loginuser() {
      // Example login logic
      if (!this.FormData.email || !this.FormData.password) {
        this.message = "Please enter email and password";
        this.messageType = "danger";
        return;
      }
      console.log("Logging in with", this.FormData.email, this.FormData.password)
      fetch('http://127.0.0.1:5000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.FormData)
      })
        .then(response => {
          if (!response.ok) {
            return response.json().then(errData => {
              throw new Error(errData.message || "Login failed");
            });
          }
          return response.json();
        })
        .then(data => {
          if (data.roles && data.roles.includes("admin")) {
            localStorage.setItem("auth_token", data.token);
            sessionStorage.setItem("roles", JSON.stringify(data.roles));
            setTimeout(() => {
              this.$router.push("/admin/dashboard");
            }, 1000); // optional delay if you want
          } else {
            this.message = data.message || "Login successful!";
            this.messageType = "success";
            localStorage.setItem("auth_token", data.token);
            sessionStorage.setItem("roles", JSON.stringify(data.roles));
            setTimeout(() => {
              this.$router.push("/user/dashboard");
            }, 1000);
          }
        })
        .then(data => console.log(data)
        )
        .catch(error => {
          this.message = error.message
          this.messageType = "danger";
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
      <h2 class="mb-4">Login</h2>

      <div class="mb-3 text-start">
        <label for="email" class="form-label">Email address</label>
        <input type="text" class="form-control" id="email" placeholder="Enter email" v-model="FormData.email"  @keyup.enter="loginuser" />
      </div>

      <div class="mb-3 text-start">
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" id="password" placeholder="Password" v-model="FormData.password"  @keyup.enter="loginuser"  />
      </div>

      <div class="d-flex justify-content-between align-items-center mb-3">
        <a href="#">Forgot password?</a>
      </div>

      <button @click="loginuser"tabindex="0" class="btn btn-primary w-100">Login</button>

      <p class="mt-3">
        Don't have an account?
        <router-link to="/signup">Sign up</router-link>
      </p>
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
