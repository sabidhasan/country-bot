<template>
  <div id="app">
    <!-- <div id="nav">
      <router-link to="/">Home</router-link> |
    </div> -->
    <router-view/>
  </div>
</template>

<style>
:root {
  --color1: bisque;
}
body {
  height: 100vh;
  max-height: 100vh;
  overflow: hidden;
  margin: 0;
  padding: 15px;
  box-sizing: border-box;
}
#app {
  height: 100%;
}
</style>
