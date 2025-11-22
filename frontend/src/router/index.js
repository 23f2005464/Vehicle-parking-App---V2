import HomePage from '@/components/pages/HomePage.vue'
import LandingPage from '@/components/pages/LandingPage.vue'
import LoginPage from '@/components/pages/LoginPage.vue'
import SignupPage from '@/components/pages/SignupPage.vue'
import BookingPage from '@/components/pages/BookingPage.vue'
import AdminPage from '@/components/pages/AdminPage.vue'
import ProfilePage from '@/components/pages/ProfilePage.vue'
import PaymentPage from '@/components/pages/PaymentPage.vue'
import SummaryPage from '@/components/pages/SummaryPage.vue'
import AdminAddLot from '@/components/pages/AdminAddLot.vue'
import AdminEditLot from '@/components/pages/AdminEditLot.vue'
import AdminSpotsPage from '@/components/pages/AdminSpotsPage.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { compile } from 'vue'



const routes=[
  {
    path: '/',
    component: LandingPage, // Layout with Navbar
  },
  {
    path: '/login',
    component: LoginPage,
    name : 'login' // No Navbar here
  },
  {
    path: '/signup',
    component:SignupPage,
    name: 'signup'
  },
  {
    path:'/user/dashboard',
    component:HomePage,
    name:'userhome'
  },
  {
    path:'/admin/dashboard',
    component:AdminPage,
    name:'AdminPage'
    
  },
  {
    path:'/user/payment/:reservation_id',
    component:PaymentPage,
    name:'PaymentPage'
  },
  {
    path:'/user/booking/:lot_id',
    component:BookingPage,
    name:'BookingPage'
  },
  {
    path:'/user/profile',
    component:ProfilePage,
    name:"ProfilePage"
  },
  {
     path:'/user/summary',
    component:SummaryPage,
    name:"SummaryPage" 
  },
  {
    path:'/admin/add_lot',
    component:AdminAddLot,
    name:"AdminAddLot"
  },
  {
     path:'/admin/edit_lot/:lot_id',
    component:AdminEditLot,
    name:"AdminEditLot"
  },
   {
    path:'/admin/spots/:lot_id',
    component:AdminSpotsPage,
    name:"AdminSpotsPage"
  },

] 




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
