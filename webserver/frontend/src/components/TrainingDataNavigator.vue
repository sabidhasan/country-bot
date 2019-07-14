<template>
  <div class="TrainingDataNavigator">
    <div class="trainingControls" :class="{'disabled': index === 1}" @click="prevPoint">
      &lt;
    </div>

    <div class="trainingPoint">
      <h1 class="trainingPointHeader">Training Point {{ index }} out of {{ totalPoints }}</h1>
      <!-- base64 src -->
      <img class="trainingImage" :src="imageSrc" alt="View from car" />
      <Histogram :data="histogram" />

      <span>Created</span>          <span>{{ created }}</span>
      <span>Command Issued</span>   <span>{{ command }}</span>
      <span>Moves</span>            <span>{{ moves }}</span>
    </div>

    <div class="trainingControls" :class="{'disabled': index === totalPoints}" @click="nextPoint">
      &gt;
    </div>
  </div>
</template>

<script>
import Histogram from '@/components/Histogram.vue';

export default {
  name: 'TrainingDataNavigator',
  components: {
    Histogram,
  },
  props: {
    totalPoints: { type: Number, required: true },
    index: { type: Number, required: true },
    created: { type: Date, required: true },
    image: { type: String, required: true },
    histogram: { type: Array, required: true },
    command: { type: String, required: true },
    moves: { type: Number, required: true },
  },
  computed: {
    imageSrc() {
      return 'data:image/jpeg;charset=utf-8;base64,' + this.image;
    },
  },
  methods: {
    nextPoint() {
      if (this.index === this.totalPoints) return;
      this.$emit('changePoint', this.index + 1);
    },
    prevPoint() {
      if (this.index === 1) return;
      this.$emit('changePoint', this.index - 1);
    },
  }
}
</script>

<style scoped>
.TrainingDataNavigator {
  display: grid; grid-template-columns: .2fr 1fr .2fr; color: var(--light);
}
.trainingControls {
  display: flex; align-items: center; justify-content: center; font-size: 11rem; color: var(--accent-dark);
}
.trainingPoint {
  padding: 10px; display: grid; grid-template-columns: 1fr 1fr;
  grid-template-rows: auto 1fr repeat(4, 1.5rem);
}
.trainingPointHeader {
  text-align: center; grid-column: 1 / -1; color: var(--accent-dark); margin: 5px 0;
}
.trainingImage {
  grid-column: 1 / -1;  border: 2px solid var(--accent-light); justify-self: center;
}
.disabled {
  color: gray; opacity: 0.4;
}
</style>
