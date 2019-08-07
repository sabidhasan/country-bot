<template>
  <div class="TrainingData">
    <NavBar />
    <!-- If no training points -->
    <div v-if="!totalPoints" class="no-data">
      <h2 class="no-data-header">NO DATA AVILABLE</h2>
      <p>Acquire some in the <router-link to="/">Drive Car</router-link> tab</p>
    </div>

    <TrainingDataNavigator v-else
      :totalPoints="totalPoints"
      :index="currIndex"
      :created="createdDate"
      :image="image_jpeg"
      :suggested_luminosity="suggested_luminosity"
      :histogram="computedHistogram"
      :command="move"
      :moves="moves"
      @changePoint="updateTrainingByIndex"
    />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import TrainingDataNavigator from '@/components/TrainingDataNavigator.vue';

export default {
  name: 'training_data',
  components: {
    NavBar,
    TrainingDataNavigator,
  },
  computed: {
    createdDate() {
      return new Date(this.created * 1000);
    },
    computedHistogram() {
      return this.histogram ? JSON.parse(this.histogram) : [];
    },
  },
  data() {
    return {
      created: null,
      image_height: 0,
      index: null,
      count: 0,
      suggested_luminosity: null,
      histogram: null,
      image_width: 0,
      ultrasonic: 0,
      image_jpeg: '',
      move: '',
      moves: 0,
      totalPoints: 0,
      currIndex: null,
    };
  },
  methods: {
    async updateTrainingByIndex(index) {
      // fetch data point by index number
      try {
        const rawData = await fetch(`/training?index=${index}`);
        const jsonData = await rawData.json();
        // Update the state
        Object.entries(jsonData)
          .map(([key, val]) => this[key] = val);
        this.currIndex = jsonData.index;
      } catch (e) {
        alert('Could not load');
      }
    },
  },
  async created() {
    // determine how many indices there are, if > 0, get first index
    var count;
    try {
      const rawCountData = await fetch('/training');
      const json = await rawCountData.json();
      count = json.count;
    } catch(e) {
      return alert('Error connecting to car server.');
    }
    if (count === 0) return;

    await this.updateTrainingByIndex(1);
    this.totalPoints = count;
    this.currIndex = 1;
  },
};
</script>

<style scoped>
.TrainingData {
  display: grid; height: 100%; grid-template-rows: auto 1fr;
}
.no-data {
  display: flex; align-items: center; justify-content: center; flex-direction: column;
  color: var(--light); margin: 0; font-size: 1.7rem;
}
.no-data-header {
  font-size: 3.6rem; color: var(--accent-light); font-size: 4.2rem;
}
</style>
