<script>
import Button from '@/components/ui/NavButton.vue'
import { routeLocationKey } from 'vue-router';
export default {
  name: 'ParkingLotsPage',
  components: {
    Button
  },
  data() {
    return {
      admindata: {},
      created_lots: [],
      loading: true,
      message: '',
      messageType: ''
    };
  },
  methods: {
    ConfirmDelete(lot_id) {
      if (confirm("Are you sure you want to delete this lot?")) {
        this.del(lot_id);
      }
    },
    del(lot_id) {
      fetch(`${this.$apiBase}/api/admin/delete_lot/${lot_id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Token-Auth': localStorage.getItem('auth_token')
        }
      })
        .then(res => res.json())
        .then(data => {
          if (data.message === "Cannot delete lot with occupied spots") {
            this.message = data.message;
            this.messageType = 'danger';
            setTimeout(() => {
              this.message = '';
            }, 2000);
            return;
          }
          this.message = data.message;
          this.messageType = 'success';
          this.created_lots = this.created_lots.filter(lot => lot.lot_id !== lot_id);

          setTimeout(() => {
            this.message = '';
            this.$router.push('/admin/dashboard');
          }, 1000)
        })
    }
  },
  mounted() {
    fetch(`${this.$apiBase}/api/auth/admin`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Token-Auth': localStorage.getItem('auth_token')
      }
    })
      .then(res => res.json())
      .then(data => {
        this.admindata = data;

        return fetch(`${this.$apiBase}/api/admin/view_lots`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Token-Auth': localStorage.getItem('auth_token')
          },
          body: JSON.stringify({ admin_id: this.admindata.id })
        });
      })
      .then(res => res.json())
      .then(data => {
        if (data.message === "No lot found for this admin ") {
          this.created_lots = []; // empty array
          this.message = data.message;
        } else {
          this.created_lots = [...data];
        }
        this.loading = false;

      })

      .catch(err => {
        console.error(err);
        alert("Error fetching admin or lots data.");
      });

  }

};
</script>



<template>
  <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger', 'text-center']"
    role="alert">
    {{ message }}
  </div>
  <h1 class="text-center mb-2 mt-4 fw-semibold fs-2">Parking lots</h1>
  <div class="container mt-1 p-4 border rounded" style="background-color: #f5f5f5;">

    <div v-if="loading" class="text-center mt-5">Loading...</div>
    <div v-else class="d-flex flex-wrap gap-3   justify-content-center">
      <div v-for="lot in created_lots" :key="lot.lot_id" class="card">
        <h5><b>{{ lot.prime_location }}</b> <img @click=" ConfirmDelete(lot.lot_id)" src="@\assets\delete.png"
            class="del-icon" width="25px">
        </h5>
        <p><strong>Lot id:</strong> {{ lot.lot_id }}</p>
        <p><strong>Pincode:</strong> {{ lot.pincode }}</p>
        <p><strong>Available Spots:</strong> {{ lot.available_spots }} / {{ lot.total_spaces }}</p>
        <p><strong>Occupied spots:</strong> {{ lot.total_spaces - lot.available_spots }}</p>
        <p><strong>Price per hour:</strong> {{ lot.price_per_hour_of_spot }}</p>

        <div class="d-flex  gap-3 justify-content-between mt-2">
          <router-link :to="{ name: 'AdminEditLot', params: { lot_id: lot.lot_id } }"><Button label=" Edit"
              radius="10px" bgcolor="#F97316" hoverColor=" #EA580C" /></router-link>
          <router-link :to="{ name:'AdminSpotsPage', params: {lot_id: lot.lot_id}  }"><Button label="Spots" height="40px" radius="10px" hoverColor="#4338CA" bgcolor="#4F46E5" /></router-link>

        </div>
      </div>
    </div>

  </div>
  <div class="button_container" >
    <div class="add_lot">
      <router-link to="/admin/add_lot"><Button label="Add lot" radius="10px" padding="5px 10px " width="15rem" fs="35px" height="60px"
          hoverColor="#008B8B" /></router-link>
    </div>
  </div>

</template>


<style scoped>
.container {
  max-width: 90vw;
  max-height: 600px;
  min-height: 600px;
  overflow-y: scroll;

}

.container::-webkit-scrollbar {
  display: none;
  /* Chrome, Safari, Opera */
}

.card {
  min-width: fit-content;
  padding: 1rem;
  text-align: justify;
  transition: all 0.3s ease;

}

.card:hover {
  box-shadow: 0 10px 20px rgba(24, 221, 239, 0.5);
  transform: translateY(-5px);
}

.card h5 {
  margin-bottom: 18px !important;
  text-align: center;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  font-size: x-large;

}

.card p {
  margin-bottom: 0.5rem !important;
  line-height: 1.3 !important;
  font-size: 15px;
}

.del-icon {
  margin-left: 1rem;
  margin-bottom: 5px;
}

.del-icon:hover {
  cursor: pointer;
  transform: scale(1.2);
  opacity: 0.8;
}

.add_lot {
  margin-top: 20px;

}

.button_container {
  display: flex;
  flex-direction: row;
  width: 100vw;
  justify-content: center;
}
</style>

