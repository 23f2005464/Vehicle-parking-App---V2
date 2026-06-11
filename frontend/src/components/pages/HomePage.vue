      <script>
      import Button from '@/components/ui/NavButton.vue'
      import { API_BASE } from "@/api";
      export default {
        name: 'HomePage',
        components: {
          Button
        },
        data() {
          return {
            userdata: '',
            userhistory: '',
            searchResults: [],
            query: '',
            search_error: '',
            DownloadButton: true
          }
        },
        methods: {
          Download_Invoice(reservationId) {
            console.log("Invoice download requested");

            const token = localStorage.getItem("auth_token");

            // STEP 1 — Start Celery Invoice Task
            fetch(`${API_BASE}/api/celery/invoice/${reservationId}`, {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
                "Token-Auth": token
              }
            })
              .then(res => res.json())
              .then(start => {
                const taskId = start.task_id;
                console.log("Invoice task started:", taskId);

                // STEP 2 — Poll Celery Status
                const interval = setInterval(() => {
                  fetch(`${API_BASE}/api/celery/get_data_invoice/${taskId}`, {
                    method: "GET",
                    headers: {
                      "Content-Type": "application/json",
                      "Token-Auth": token
                    }
                  })
                    .then(res => res.json())
                    .then(PollData => {
                      console.log("Invoice status:", PollData);

                      if (PollData.status === "pending") return; // keep polling

                      clearInterval(interval); // stop once done

                      if (PollData.status === "error") {
                        console.error("Invoice generation failed:", PollData.message);
                        return;
                      }

                      // INVOICE READY -> status.token contains the signed token
                      if (PollData.status === "ready") {
                        const url =
                          `${API_BASE}/api/celery/download_invoice?token=` + PollData.token;

                        console.log("Downloading invoice:", url);

                        window.open(url, "_blank"); // Trigger download
                      }
                    })
                    .catch(err => {
                      clearInterval(interval);
                      console.error("Polling failed:", err);
                    });
                }, 500);
              })
              .catch(err => {
                console.error("Invoice task creation failed:", err);
              });
          },

          Download_csv() {
            console.log("Download requested");

            const token = localStorage.getItem("auth_token");
            const userId = this.userdata.user_id;

            // STEP 1 — Start Celery CSV task
            fetch(`${API_BASE}/api/celery/user_create_csv/` + userId, {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
                "Token-Auth": token
              }
            })
              .then(res => res.json())
              .then(start => {
                const taskId = start.task_id;
                console.log("CSV task started:", taskId);

                // STEP 2 — Poll Celery status
                const interval = setInterval(() => {

                  fetch(`${API_BASE}/api/celery/get_data/` + taskId, {
                    method: "GET",
                    headers: {
                      "Content-Type": "application/json",
                      "Token-Auth": token
                    }
                  })
                    .then(res => res.json())
                    .then(status => {
                      console.log("Status:", status);

                      // Still processing → wait
                      if (status.status === "pending") return;

                      clearInterval(interval);   // stop polling once done

                      // Error case
                      if (status.status === "error") {
                        console.error("CSV generation failed:", status.message);
                        return;
                      }

                      // Ready → download file
                      if (status.status === "ready") {
                        const url =
                          `${API_BASE}/api/celery/download_csv?token=` + status.token;

                        console.log("Downloading:", url);

                        // Window-based file download (your requirement)
                        window.open(url, "_blank");
                      }
                    })
                    .catch(err => {
                      clearInterval(interval);
                      console.error("Polling failed:", err);
                    });

                }, 500);
              })
              .catch(err => {
                console.error("Task creation failed:", err);
              });
          },




          handleSearch() {
            this.searchNotHide = true;
            this.search_error = ''; // clear previous error
            fetch(`${API_BASE}/api/user/searching_lots`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Token-Auth': localStorage.getItem('auth_token')
              },
              body: JSON.stringify({ "pincode": this.query })
            })
              .then(response => response.json().then(data => ({ status: response.status, body: data })))
              .then(({ status, body }) => {
                if (status === 404 || body.message) {
                  this.search_error = body.message || "No results found.";
                  this.searchResults = [];
                } else {
                  this.searchResults = body;
                  this.search_error = '';
                }
              })
              .catch(err => {
                console.error('Error fetching search results:', err);
                this.search_error = 'Search failed.';
                this.searchResults = [];
              });

            this.query = '';
          }
        }
        ,
        mounted() {
          const token = localStorage.getItem('auth_token');

          const userFetch = fetch(`${API_BASE}/api/auth/user`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Token-Auth': token
            }
          }).then(res => res.json());

          const historyFetch = fetch(`${API_BASE}/api/user/my_reservations`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Token-Auth': token
            }
          }).then(res => res.json());

          Promise.all([userFetch, historyFetch])
            .then(([userData, historyData]) => {
              this.userdata = userData;
              if (historyData.message === "No reservations found") {
                this.userhistory = []; // convert to empty array
                this.DownloadButton = false;
                return;
              }

              // CASE 2: User has reservations
              this.userhistory = historyData;

              // Check if user paid at least once
              const anyPaid = this.userhistory.some(item => item.total_amount_user_paid !== 0);

              this.DownloadButton = anyPaid;


              return fetch(`${API_BASE}/api/user/searching_lots`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Token-Auth': token
                },
                body: JSON.stringify({
                  "pincode": this.userdata.pincode
                })
              });
            })
            .then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(({ status, body }) => {
              if (status === 404 || body.message) {
                this.search_error = body.message || "No results found.";
                this.searchResults = [];
              } else {
                this.searchResults = body;
                this.search_error = '';
              }
            })
            .catch(err => {
              console.error('Error fetching data:', err);
            });
        }


      }
</script>
      <template>
        <div v-if="message"
          :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger', 'text-center']" role="alert">
          {{ message }}
        </div>



        <div class="container  ">
          <h4 class="mb-4 justify-content-center d-flex fw-bold">Search Parking Locations</h4>
          <div class="d-flex justify-content-center">
            <input v-model="query" class="form-control me-2 custom-input" type="text" placeholder="Enter location..." />
            <Button label="Search" @click="handleSearch()" />
          </div>
          <div v-if="search_error" class="alert alert-warning mt-3">
            {{ search_error }}
          </div>

          <div class="container card-container">
           <div v-if="searchResults.length === 0">
           <img src="frontend/src/assets/Userhomepage.png">
           </div>
            <div v-for="(lot, index) in searchResults" :key="index">
              <div class="card" style="width: 18rem;">
                <div class="card-body search-card">
                  <h5 class="card-title">
                    #Lot {{ lot.lot_id }} Available Spots: {{ lot.available_spots }}
                  </h5>
                  <h6 class="card-subtitle text-body-secondary">
                    Area: {{ lot.prime_location }}
                  </h6>
                  <h6 class="card-subtitle text-body-secondary">
                    Address: {{ lot.address }}
                  </h6>
                  <h6 class="card-subtitle text-body-secondary">
                    Pincode: {{ lot.pincode }}
                  </h6>
                  <h5 class="card-subtitle mb-2 text-body-secondary">
                    <b>Price</b>: {{ lot.price_per_hour_of_spot }}
                  </h5>

                  <router-link :to="`/user/booking/${lot.lot_id}`"><Button label="Book" radius="10px"
                      bgcolor="#007bff" /></router-link>
                </div>
              </div>
            </div>
          </div>

          <div class="history-header">
            <h2 class="mt-4">History</h2>
            <h5 class="download-row"
             v-if="DownloadButton === true && userhistory.length > 0">
              <span>Download Paid Reservations History</span>
              <Button label="Download" height="40px" radius="10px" color="Black" @click.native="Download_csv" />
            </h5>

          </div>

          <div class="history-con">
            <div v-if="userhistory.length === 0">
              <h1 style="color: Red;">No Reservations Yet </h1>
            </div>
            <div v-else
              v-for="(item, index) in userhistory" :key="index">
              <div class="card" style="width: 18rem;height: 289.6px;">
                <div class="card-body">
                  <h5 class="card-title">{{ item.prime_location }} (Res.Id-{{ item.reservation_id }})</h5>
                  <h6 class="card-subtitle mb-2 text-body-secondary">Lot Id: {{ item.lot_id }} </h6>
                  <h6 class="card-subtitle mb-2 text-body-secondary">Address: {{ item.address }} </h6>
                  <h6 class="card-subtitle mb-2 text-body-secondary">Vehicle: {{ item.vehicle_number }}</h6>
                  <h6 class="card-subtitle mb-2 text-body-secondary">Spot: {{ item.lot_id }} -{{ item.spot_id }} </h6>
                  <h6 class="card-subtitle mb-2 text-body-secondary">Parked on : {{ item.parking_timestamp }}</h6>

                  <a class="card-link" v-if="item.total_amount_user_paid == 0"><router-link
                      :to="`/user/payment/${item.reservation_id}`"><Button label="Pay"
                        radius="10px" /></router-link></a>

                  <div v-else>
                    <h6 class="card-subtitle mb-1 text-body-secondary">Parked out : {{ item.end_parking_timestamp }}
                    </h6>
                    <div class="mt-2"> <Button label="invoice" @click.prevent="Download_Invoice(item.reservation_id)"
                        radius="10px" bgcolor="#20C997" /></div>
                  </div>

                </div>

              </div>


            </div>
          </div>

        </div>



      </template>
<style scoped>
.custom-searchbar {
  width: 90%;
  max-width: 40rem;
  height: 3rem;
  background-color: #f6f3f3;
  border: solid 2px;
  border-radius: 30px;
}

.history-con {
  min-height: 200px;
  max-height: 500px;
  overflow-y: scroll;
  overflow-x: hidden;
  margin-top: 20px;
  padding-right: 10px;
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  justify-content: space-evenly;
  scrollbar-width: none;
  gap: 0.5rem;

}

.history-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

.download-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 1rem;
  margin-right: 1rem;
}

.card-container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
  margin-top: 20px;
  max-height: 600px;
  min-height: 600px;
  overflow-y: scroll;
  background-color: #edf2fb;
  padding: 2rem;
  border-radius: 20px;
  scrollbar-width: none;
}

.card {
  flex: 1 1 300px;
  max-width: 350px;
  min-width: 280px;
  min-height: 270px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}


.card-body {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.search-card {
  justify-content: space-around;
}

</style>
