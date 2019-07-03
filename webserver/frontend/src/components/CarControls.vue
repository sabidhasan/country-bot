<template>
  <div class="car_controls">
    <button :disabled="commandInProgress" class="ctrl_button" @click="goLeft">
      LEFT
    </button>
    <button :disabled="commandInProgress" class="ctrl_button" @click="goForward">
      FORWARD
    </button>
    <button :disabled="commandInProgress" class="ctrl_button" @click="goRight">
      RIGHT
    </button>
  </div>
</template>

<script>
function keyPressListener({ key } = e) {
  switch (key) {
    case 'ArrowUp':
    case 'w':
      this.goForward();
      break;
    case 'ArrowLeft':
    case 'a':
      this.goLeft();
      break;
    case 'ArrowRight':
    case 'd':
      this.goRight();
      break;
  };
}

export default {
  name: 'CarControls',
  created() {
    window.addEventListener('keydown', keyPressListener.bind(this));
  },
  beforeDestroy() {
    window.removeEventListener('keydown', keyPressListener.bind(this));
  },
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
  props: {
    commandInProgress: { type: Boolean },
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
.ctrl_button:disabled {
  background: gray;
}
.ctrl_button {
  border: 1px solid black;
  background: var(--color1);
  padding: 12px;
  font-size: 1.5rem;
  font-weight: bold;
  width: 20%;
}
@media screen and (max-width: 500px) {
  .car_controls button {
    width: auto;
  }
}
</style>
