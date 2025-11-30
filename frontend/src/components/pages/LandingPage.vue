<script>
export default {
  name: "LandingPage",
  data() {
    return {
      images: [
        "/src/assets/parking.jpg",
        "/src/assets/man.jpg",
        "/src/assets/trip.webp"
      ],
      index: 0
    };
  },
  mounted() {
    setInterval(() => {
      this.index = (this.index + 1) % this.images.length;
    }, 2500);
  }
};
</script>

<template>
  <div class="smt-container"> 
    <div class="logo-box"> 
       <img src="@/assets/logo.png" class="logo fade-loop" />
    </div>

    <h1>Stop Guessing. Start Parking.</h1>
  </div>
    
  <div class="container">
    <div class="slideshow-box">
      <img :src="images[index]" class="slide-img" />
    </div>
    
  </div>
  <section class="feature-section" aria-labelledby="features-heading">
  <h2 id="features-heading" class="feature-title">Platform Capabilities</h2>

  <div class="feature-grid">

    <div class="feature-card">
      <h3>Email Reminders</h3>
      <p>Automatic reminders for upcoming bookings, expiry alerts, and overdue notifications sent directly to users.</p>
    </div>

    <div class="feature-card">
      <h3>Admin Lot Management</h3>
      <p>Admins control all parking lots, floors, pricing rules, slot types, and operational settings from a unified panel.</p>
    </div>

    <div class="feature-card">
      <h3>Beautiful Dashboard</h3>
      <p>A clean, responsive dashboard with real-time occupancy, revenue updates, and quick operational views.</p>
    </div>

    <div class="feature-card">
      <h3>Analytical Dashboard</h3>
      <p>Advanced analytics including trends, heatmaps, hourly statistics, and performance insights for informed decisions.</p>
    </div>

    <div class="feature-card">
      <h3>Flask Security System</h3>
      <p>Backend powered by Flask with secure APIs, and protected authentication flows.</p>
    </div>

    <div class="feature-card">
      <h3>Monthly Reports</h3>
      <p>Download monthly summaries including revenue, reservations, user stats, and occupancy reports in PDF/CSV.</p>
    </div>

    <div class="feature-card">
      <h3>Booking & Payments</h3>
      <p>Users can reserve parking spots and pay securely .</p>
    </div>

    <div class="feature-card">
      <h3>Role-Based Access</h3>
      <p>Role management for admin, staff, security, and users with detailed activity logs and data protection.</p>
    </div>

  </div>
</section>


</template>

<style scoped>
.container {
  width: 100%;
  background-color: #fff;
  height: 700px;
  margin-top: 1rem;
  border-radius: 20px;
  box-shadow: 0 0 10px black;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.smt-container{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.smt-container h1{
  font-weight: bold;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* ---------- LOGO ----------- */
.logo-box {
  margin-bottom: 1rem;
  width: 200px;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo {
  width: 120px;
  height: 80px;
  margin-top: 1.5rem;
}

.fade-loop {
  animation: fadeLoop 60s infinite ease-in-out;
}

@keyframes fadeLoop {
  0%   { opacity: 0; }
  20%  { opacity: 1; }  
  80%  { opacity: 1; }  
  100% { opacity: 0; }  
}

.slideshow-box {
  width: 100%;
  height: 100%;
  margin-top: 1.5rem;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.slide-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
/* Feature Section */
.feature-section {
  width: 100%;
  margin-top: 0rem;
  padding: 1.5rem 1rem;
  text-align: center;
}

.feature-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #222;
}

/* Grid Layout */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.5rem;
  padding: 0 1rem;
}

/* Feature Card */
.feature-card {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  transition: 0.3s ease;
  text-align: left;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

.feature-card h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.4rem;
  color: #1a1a1a;
}

.feature-card p {
  color: #555;
  font-size: 0.95rem;
  line-height: 1.4rem;
}

</style>
