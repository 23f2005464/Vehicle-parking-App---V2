<script>
import Button from '@/components/ui/NavButton.vue'

export default {
  name: 'BookingPage',
  components: { Button },

  data() {
    return {
      bookingData: {},
      vehicle_number: '',
      message: '',
      messageType: ''
    }
  },

  mounted() {
    const lot_id = this.$route.params.lot_id;

    // Fetch preview info for available spot
    fetch('http://127.0.0.1:5000/api/user/issuing_spot/preview', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Token-Auth': localStorage.getItem('auth_token')
      },
      body: JSON.stringify({ lot_id: lot_id })
    })
      .then(response => response.json())
      .then(data => {
        console.log('Preview Data:', data);
        if (data.lot_info) {
          this.bookingData = data.lot_info;
        } else {
          console.error('Error fetching spot info:', data.message);
        }
      })
      .catch(err => console.error('Error fetching preview:', err));
  },

  methods: {
    BookSpot() {
      if (!this.vehicle_number) {
        alert("Please enter your vehicle number before booking.");
        return;
      }

      fetch('http://127.0.0.1:5000/api/user/issuing_spot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Token-Auth': localStorage.getItem('auth_token')
        },
        body: JSON.stringify({
          lot_id: this.bookingData.lot_id,
          vehicle_number: this.vehicle_number
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data.message === "Spot reserved successfully") {
            this.message = data.message;
            this.messageType = "success";
            console.log("Reservation Details:", data.reservation_details);

            // Redirect after booking success
            setTimeout(() => {
              this.$router.push("/user/dashboard");
            }, 1500);
          } else {
            console.error("Booking failed:", data);
          }
        })
        .catch(err => console.error('Error during booking:', err));
    }
  }
}
</script>

<template>
  <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger','text-center'] " role="alert">
  {{ message }}
</div>

  <div>
   
    <div class="payment-container">
      <h1 class="page-title">Book Your Parking Spot</h1>

      <div v-if="bookingData.spot_id>=0">
        <div class="mb-3 row">
          <label class="col-sm-4 label-text">Lot ID:</label>
          <div class="col-sm-8">
            <div class="value-box">{{ bookingData.lot_id }}</div>
          </div>
        </div>

        <div class="mb-3 row">
          <label class="col-sm-4 label-text">Spot ID:</label>
          <div class="col-sm-8">
            <div class="value-box">{{ bookingData.spot_id }}</div>
          </div>
        </div>

        <div class="mb-3 row">
          <label class="col-sm-4 label-text">Vehicle Number:</label>
          <div class="col-sm-8">
            <input
              v-model="vehicle_number"
              class="value-box"
              type="text"
              placeholder="Enter vehicle number"
            />
          </div>
        </div>

        <div class="btn-group-custom">
          <Button @click="BookSpot" label="Book Spot"></Button>
          <router-link to="/user/dashboard">
            <Button label="Cancel"></Button>
          </router-link>
        </div>
      </div>

      <div v-else>
        <p class="text-center">Fetching available spot details...</p>
      </div>
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
