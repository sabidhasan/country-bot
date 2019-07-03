<template>
  <div id="app">
    <!-- <div id="nav">
      <router-link to="/">Home</router-link> |
    </div> -->
    <router-view/>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css?family=Raleway:200,400,500&display=swap');
:root {
  --dark: #22201c;
  --accent-dark: #a33327;
  --accent-light: #689675;
  --light: #ad8173;
}
body {
  font-family: 'Raleway', sans-serif; height: 100vh; padding: 15px;
  max-height: 100vh; overflow: hidden; margin: 0; box-sizing: border-box;
}
#app {
  height: 100%;
}
@media screen and (max-width: 500px) {
  padding: 5px;
}
</style>
