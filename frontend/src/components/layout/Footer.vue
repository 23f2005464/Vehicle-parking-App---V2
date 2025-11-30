<template>
    <footer class="footer">
  <div class="footer-container">

    <!-- Column 1: Brand -->
    <div class="footer-col">
      <h2 class="footer-logo">PMS| Parking Management System</h2>
      <p class="footer-text">
        Smart Parking Management System with booking, payments, analytics, and automated reminders.
      </p>
    </div>

    <!-- Column 2: Quick Links -->
    <div class="footer-col">
      <h3>Quick Links</h3>
      <ul class="footer-links">
        <li><a href="#">Home</a></li>
        <li><a href="#">Features</a></li>
        <li><a href="#">Dashboard</a></li>
        <li><a href="#">Pricing</a></li>
      </ul>
    </div>

    <!-- Column 3: Support -->
    <div class="footer-col">
      <h3>Support</h3>
      <ul class="footer-links">
        <li><a href="#">Help Center</a></li>
        <li><a href="#">Report Issue</a></li>
        <li><a href="#">API Docs</a></li>
      </ul>
    </div>

    <!-- Column 4: Contact -->
    <div class="footer-col">
      <h3>Contact</h3>
      <ul class="footer-links">
        <li><span>Email:</span> support@pms.com</li>
        <li><span>Location:</span> India</li>
      </ul>
    </div>

  </div>

  <div class="footer-bottom">
    <p>© 2025 PMS. All rights reserved.</p>
  </div>
</footer>

</template>
<style scoped>
/* Footer */
.footer {
  width: 100%;
  background: #0f172a;
  color: #e2e8f0;
  margin-top: 2.5rem;
  padding: 2.5rem 1.5rem 1rem;
}

.footer-container {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 2rem;
  max-width: 1200px;
  margin: auto;
}

.footer-col h2.footer-logo {
  font-size: 2rem;
  font-weight: 800;
  color: #fff;
  margin-bottom: 0.6rem;
}

.footer-col h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 0.6rem;
}

.footer-text {
  width: 260px;
  font-size: 0.95rem;
  color: #cbd5e1;
  line-height: 1.4rem;
}

/* Links */
.footer-links {
  list-style: none;
  padding: 0;
}

.footer-links li {
  margin: 0.4rem 0;
  font-size: 0.9rem;
  color: #cbd5e1;
}

.footer-links a {
  color: #cbd5e1;
  text-decoration: none;
}

.footer-links a:hover {
  text-decoration: underline;
  color: #fff;
}

/* Bottom line */
.footer-bottom {
  text-align: center;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255,255,255,0.15);
}

.footer-bottom p {
  font-size: 0.85rem;
  color: #94a3b8;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .footer-container {
    flex-direction: column;
  }
}

</style>