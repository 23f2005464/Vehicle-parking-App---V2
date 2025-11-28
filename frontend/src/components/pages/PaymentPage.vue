<script>import Button from '@/components/ui/NavButton.vue'
export default {
  name: 'PaymentPage',
  components: {
    Button,
  },
  data() {
    return {
      paymentData: '',
      message: '',
      messageType: ''
    }

  },
  methods: {
    Payfunction() {
      fetch("http://127.0.0.1:5000/api/user/paying_transaction", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Token-Auth': localStorage.getItem('auth_token')
        },
        body: JSON.stringify({
          reservation_id: this.paymentData.reservation_id,
          amount_user_paid: this.paymentData.amount,
          parking_end: new Date(this.paymentData.parking_end).toISOString(),
          duration: this.paymentData.duration
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data.message === "successfully paid") {
            this.message = data.message;
            this.messageType = "success";

            setTimeout(() => {
              this.$router.push("/user/dashboard");
            }, 1400);
          } else {
            this.message = data.error || "Payment failed";
            this.messageType = "error";
          }
        })
        .catch(error => {
          console.error('Error during payment:', error)
          this.message = 'Network error during payment.'
          this.messageType = 'error'
        })
    }
  },
  mounted() {
    fetch("http://127.0.0.1:5000/api/user/pay_now", {
      method: 'POST',

      headers: {
        'Content-Type': 'application/json',
        'Token-Auth': localStorage.getItem('auth_token')
      },
      body: JSON.stringify({
        "reservation_id": this.$route.params.reservation_id
      })
    })
      .then(response => response.json())
      .then(data => this.paymentData = data)

      .catch(error => {
        console.error('Error during login:', error)
        alert("An error occurred during login.")
      })
  }
}
</script>
<template>
 <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger','text-center'] " role="alert">
  {{ message }}
</div>

  <div class="payment-container">
    <h1 class="page-title">Payment Gateway</h1>

    <div class="mb-3 row">
      <label class="col-sm-3 label-text">Your Name:</label>
      <div class="col-sm-9">
        <div class="value-box">{{ paymentData.fullname }}</div>
      </div>
    </div>

    <div class="mb-3 row">
      <label class="col-sm-3 label-text">Email:</label>
      <div class="col-sm-9">
        <div class="value-box">{{ paymentData.email }}</div>
      </div>
    </div>

    <div class="mb-3 row">
      <label class="col-sm-3 label-text">Duration (hr):</label>
      <div class="col-sm-9">
        <div class="value-box">{{ paymentData.duration }}</div>
      </div>
    </div>

    <div class="mb-3 row">
      <label class="col-sm-3 label-text">Parked Time:</label>
      <div class="col-sm-9">
        <div class="value-box">{{ paymentData.parking_start }}</div>
      </div>
    </div>

    <div class="mb-3 row">
      <label class="col-sm-3 label-text">Releasing Time:</label>
      <div class="col-sm-9">
        <div class="value-box">{{ paymentData.parking_end }}</div>
      </div>
    </div>

    <div class="mb-4 row">
      <label class="col-sm-3 label-text">Bill Amount:</label>
      <div class="col-sm-9">
        <div class="value-box">{{ paymentData.amount }}</div>
      </div>
    </div>

    <div class="btn-group-custom">
      <Button @click="Payfunction" label="Pay"></Button>
      <a><router-link to="/user/dashboard"><Button label="Cancel"></Button></router-link></a>
    </div>
  </div>


</template>
<style>
body {
  font-family: 'Montserrat', sans-serif;
  background-color: #f8f9fa;
}

.payment-container {
  max-width: 800px;
  margin: 4rem auto;
  background-color: #fff;
  border: 2px solid black;
  border-radius: 20px;
  padding: 2rem 3rem;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.page-title {
  text-align: center;
  font-weight: 700;
  margin-bottom: 2rem;
}

.label-text {
  font-weight: 600;
  font-size: 1.1rem;
}

.value-box {
  font-size: 1rem;
  border: 1.5px solid #686060;
  border-radius: 8px;
  background-color: #fdfdfd;
  padding: 0.75rem;
  width: 100%;
}

.btn-primary {
  background-color: black;
  border-color: black;
  font-weight: 600;
  font-size: 1.1rem;
}

.btn-primary:hover {
  background-color: #048002;
  border-color: #222831;
}

.btn-custom {
  width: 8rem;
  border-radius: 8px;
  font-weight: 700;
  color: #D9D9D9;
}

.btn-custom:hover {
  background-color: #898989;
  color: black;
}

.btn-group-custom {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}
</style>