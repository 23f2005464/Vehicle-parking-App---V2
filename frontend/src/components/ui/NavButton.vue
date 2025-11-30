<script setup>
defineProps({
  label: {
    type: String,
    default: 'Edit Profile'
  },
  radius: {
    type:String,
    default:'25px'
  },
  bgcolor:{
    type:String,
    default:"#161d26"
  },
  hoverColor: {
     type: String,
     default: '#00bcd4' },
  width: {
     type: String,
     default: '120px'
     },    
  padding:{
    type:String,
    default:'8px'
  },
  fs:{
    type:String,
    default:'15px'
  },
  height:{
    type:String,
    default:'40px'}
  
 
})
</script>


<template>
    <div class="nav-button">
        <button type="button" class="btn btn-primary btn-lg" :style="{ 'border-radius': radius,
      'background-color': bgcolor, 'width': width,'padding':padding,'font-size':fs,'height':height,
      '--hover-color': hoverColor}">{{ label }}</button>
    </div>
    
</template>
<style scoped>
.nav-button{
  margin : 0px 0px 0px 0px;
  
}
.btn-primary{
  background-color: #161d26;
  color: #fff;
  border: none;
 transition: background-color 0.3s ease-in-out;
  font-weight: bold;
 


}
.btn-primary:hover{
  background:var(--hover-color) !important;
  color: #000;
 
}

.btn {
    
  text-align: center; /* keeps text centered */
}
</style>