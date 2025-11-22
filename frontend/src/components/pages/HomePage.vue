      <script>
      import Button from '@/components/ui/NavButton.vue'
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
            searchNotHide: false,
            query: '',
            search_error: '',
          }
        },
        methods: {
          handleSearch() {
            this.searchNotHide = true;
            this.search_error = ''; // clear previous error
            fetch("http://localhost:5000/api/user/searching_lots", {
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

          const userFetch = fetch("http://localhost:5000/api/auth/user", {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Token-Auth': token
            }
          }).then(res => res.json());

          const historyFetch = fetch("http://localhost:5000/api/user/my_reservations", {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Token-Auth': token
            }
          }).then(res => res.json());

          Promise.all([userFetch, historyFetch])
            .then(([userData, historyData]) => {
              this.userdata = userData;
              this.userhistory = historyData;

              return fetch("http://localhost:5000/api/user/searching_lots", {
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
                this.searchNotHide = false;
              } else {
                this.searchResults = body;
                this.search_error = '';
                this.searchNotHide = true;
              }
            })
            .catch(err => {
              console.error('Error fetching data:', err);
              alert('An error occurred while loading the page.');
            });
        }


      }
</script>
      <template>
<div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-danger','text-center'] " role="alert">
  {{ message }}
</div>



        <div class="container  ">
          <h4 class="mb-4 ">Search Parking Locations</h4>
          <div class="d-flex justify-content-center">
            <input v-model="query" class="form-control me-2 custom-input" type="text" placeholder="Enter location..." />
            <Button label="Search" @click="handleSearch()" />
          </div>
          <div v-if="search_error" class="alert alert-warning mt-3">
            {{ search_error }}
          </div>
          <div v-if="searchNotHide">
            <div class="row searchres-container mt-5">
              <div class="col-md-4 mb-4" v-for="(lot, index) in searchResults" :key="index">
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
          </div>
          <h2 class="mt-4">History</h2>
          <div class="row history-con">

            <div class="col-md-4 mb-4" v-for="(item, index) in userhistory" :key="index">
              <div class="card" style="width: 18rem;">
                <div class="card-body">
                  <h5 class="card-title">{{ item.prime_location }} (Id-{{ item.reservation_id }})</h5>
                  <h6 class="card-subtitle mb-2 text-body-secondary">Address: {{ item.address }} </h6>
                  <h6 class="card-subtitle mb-2 text-body-secondary">Vehicle: {{ item.vehicle_number }}</h6>
                  <!-- <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card’s
                    content.</p> -->
                  <h6 class="card-subtitle mb-2 text-body-secondary">Spot: {{ item.lot_id }} -{{ item.spot_id }} </h6>
                  <h6 class="card-subtitle mb-2 text-body-secondary">Parked on : {{ item.parking_timestamp }}</h6>

                  <a class="card-link" v-if="item.total_amount_user_paid == 0"><router-link
                      :to="`/user/payment/${item.reservation_id}`"><Button label="Pay"
                        radius="10px" /></router-link></a>

                  <div v-else>
                    <h6 class="card-subtitle mb-1 text-body-secondary">Parked out : {{ item.end_parking_timestamp }}
                    </h6>
                    <div class="mt-2"> <Button label="invoice" radius="10px" bgcolor="#20C997" /></div>
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
  /* minimum visible area */
  max-height: 500px;
  /* maximum height limit */
  overflow-y: scroll;
  /* enable vertical scrolling */
  overflow-x: hidden;
  /* prevent horizontal scroll */
  margin-top: 20px;
  padding-right: 10px;
  /* avoids scrollbar overlap */
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  scrollbar-width: none;
}


.row {
  margin-left: 35px;
  /* adds your left margin */
  max-height: 600px;
  /* optional: gives it height */
  display: flex;
  /* ensure flex layout */
  flex-wrap: wrap;
  /* allows wrapping to next line */
  /* adds spacing between cards */
  justify-content: flex-start;
}

.searchres-container {
  min-height: 100px;
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: center;
}

.card {
  flex: 1 1 300px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 270px;
  /* adjust for consistent height */
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