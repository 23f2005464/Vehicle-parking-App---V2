<script>
import { useRoute } from 'vue-router'
import NavBar from '@/components/layout/Navbar.vue'
import UserNavbar from './components/layout/UserNavbar.vue';
import AdminNavbar from './components/layout/AdminNavbar.vue';

export default {
  name: 'App',

  components: {
    NavBar,
    UserNavbar,
    AdminNavbar
  },

  setup() {
    // Composition API inside Options API — useRoute() must stay here
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
</template>
  
<style scoped></style>
