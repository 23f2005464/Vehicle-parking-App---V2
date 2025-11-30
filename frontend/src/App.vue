<script>
import { useRoute } from 'vue-router'
import NavBar from '@/components/layout/Navbar.vue'
import UserNavbar from './components/layout/UserNavbar.vue';
import AdminNavbar from './components/layout/AdminNavbar.vue';
import Footer from './components/layout/Footer.vue';
export default {
  name: 'App',

  components: {
    NavBar,
    UserNavbar,
    AdminNavbar,
    Footer
  },

  setup() {
    const route = useRoute()
    return { route }
  }
}
</script>

<template>
  <UserNavbar v-if="route.path.startsWith('/user')"/>
  <AdminNavbar v-if="route.path.startsWith('/admin')" />
  <NavBar v-if = "route.path === '/'" />
  <router-view  />
  <Footer v-if="route.path.startsWith('/user') ||route.path.startsWith('/admin') || route.path === '/' "  />
</template>
  
<style scoped></style>
