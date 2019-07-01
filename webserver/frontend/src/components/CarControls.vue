<template>
  <div class="car_controls">
    <button class="car_control_button" @click="goLeft">LEFT</button>
    <button class="car_control_button" @click="goForward">FORWARD</button>
    <button class="car_control_button" @click="goRight">RIGHT</button>
  </div>
</template>

<script>

export default {
  name: 'CarControls',
  methods: {
    goLeft() {
      this.$emit('move', 'l');
    },
    goRight() {
      this.$emit('move', 'r');
    },
    goForward() {
      this.$emit('move', 'f');
    },
  },
};
</script>

<style scoped>
  .car_controls {
    grid-column: 1 / -1;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
  }
  .car_control_button {
    border: 1px solid black;
    background: var(--color1);
    padding: 12px;
    font-size: 1.5rem;
    font-weight: bold;
    width: 20%;
  }
</style>
