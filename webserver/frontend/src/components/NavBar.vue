<template>
  <div class="nav-container">
    <h1>CountryBot</h1>
    <nav>
      <router-link to="/" class="nav_item">Drive Car</router-link>
      <router-link to="/" class="nav_item">Train Car</router-link>
      <router-link to="/" class="nav_item">Self Drive</router-link>
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
h1 {
  color: var(--accent-dark); letter-spacing: 5px; font-size: 2.2rem;
}
.nav-container {
  display: flex; justify-content: space-between; grid-column: -1 / 1; margin-bottom: 15px;
}
nav {
  display: flex; align-items: center; justify-content: space-around;
  width: 100%; max-width: 55%; min-width: 330px;
}
.nav_item {
  color: var(--accent-light); font-size: 1.5rem; text-decoration: none;
  font-weight: bold;
}
@media screen and (max-width: 500px) {
  h1 {
    margin: 0; font-size: 1.4rem; text-align: center; width: 100%;
  }
  .nav-container {
    display: grid; width: 100%; grid-template-columns: 1fr;
  }
  nav {
    justify-self: center; margin-top: 10px;
  }
}
</style>
