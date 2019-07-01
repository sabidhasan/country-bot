<template>
  <div class="nav">
    <h2>CountryBot</h2>
    <nav>
      <router-link to="/" class="nav_item">Drive Car</router-link>
      <router-link to="/" class="nav_item">Train Car</router-link>
      <router-link to="/" class="nav_item">Self Driving Mode</router-link>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'NavBar',
  props: {
  },
};
</script>

<style scoped>
h2 {
  margin-right: 50%;
}
.nav {
  display: flex;
  grid-column: -1 / 1;
}
nav {
  display: flex; align-items: center; justify-content: space-around;
  width: 100%;
}
</style>
