<template>
  <div class="TrainingDataNavigator">
    <div class="trainingControls" :class="{'disabled': index === 1}" @click="prevPoint">
      &lt;
    </div>

    <div class="trainingPoint">
      <h1 class="trainingPointHeader">
        Training Point
        <input
          type="text" class="edit-index" :class="{ hide : !editIndex }" ref="editIndexBox"
          v-model="userPickedIndex" @keyup.enter="changeId"
        />
        <span class="index" :class="{ hide: editIndex }" @click="this.editIndex = true">{{ index }} </span>
        out of {{ totalPoints }}
        <!-- <small @click="changeId">Go to Point</small> -->
      </h1>
      <!-- base64 src -->
      <img class="trainingImage" :src="imageSrc" alt="View from car" />
      <Histogram :data="histogram" :label="histogramLabel" />

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
  data() {
    return {
      userPickedIndex: this.index,
      editIndex: false,
    };
  },
  props: {
    totalPoints: { type: Number, required: true },
    index: { type: Number, required: true },
    created: { type: Date, required: true },
    image: { type: String, required: true },
    suggested_luminosity: { type: Number, required: true },
    histogram: { type: Array, required: true },
    command: { type: String, required: true },
    moves: { type: Number, required: true },
  },
  computed: {
    imageSrc() {
      return `data:image/jpeg;charset=utf-8;base64,${this.image}`;
    },
    histogramLabel() {
      return `Histogram calculated at luminosity ${this.suggested_luminosity.toFixed(3)}`;
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
    changeId() {
      const nInd = this.userPickedIndex;
      if (!nInd || Number.isNaN(parseInt(nInd, 10)) || nInd <= 0 || nInd > this.totalPoints) return;
      // Update the index, hide the box
      this.$emit('changePoint', parseInt(nInd, 10));
      this.editIndex = false;
    },
  },
};
</script>

<style scoped>
.TrainingDataNavigator {
  display: grid; grid-template-columns: .2fr 1fr .2fr; color: var(--light);
}
.hide {
  display: none;
}
.index {
  text-decoration-line: underline; text-decoration-style: dotted; font-size: 32px;
  width: 5rem; text-align: center; border: 2px var(--accent-light) dotted; background: var(--dark);
  color: var(--light);
}
.edit-index {
  color: var(--accent-dark); font-size: 2.3rem; margin: 0 0px; width: 4rem; text-align: center;
  border: 0; background: var(--dark); font-family: Raleway,sans-serif; font-weight: bold;
}
.trainingControls {
  display: flex; align-items: center; justify-content: center;
  font-size: 11rem; color: var(--accent-dark);
}
.trainingPoint {
  padding: 10px; display: grid; grid-template-columns: 1fr 1fr;
  grid-template-rows: auto 3fr 2fr repeat(3, 1.5rem);
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
