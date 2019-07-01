<template>
  <div class="home">
    <NavBar />
    <h1 class="title">Country-Bot</h1>
    <CarView />
    <CarStats :odometer="odometer" :sensor="sensor" :moves="moves" :created="created" :id="id" />
    <CarControls @move="handleMove"/>
  </div>
</template>

<script>
// @ is an alias to /src
import NavBar from '@/components/NavBar.vue';
import CarView from '@/components/CarView.vue';
import CarStats from '@/components/CarStats.vue';
import CarControls from '@/components/CarControls.vue';

export default {
  name: 'home',
  components: {
    NavBar,
    CarView,
    CarStats,
    CarControls,
  },
  data() {
    return {
      odometer: 0,
      sensor: 0,
      moves: 0,
      created: null,
      id: null,
    };
  },
  methods: {
    async handleMove(direction) {
      const validMoves = ['f', 'r', 'l'];
      if (!validMoves.includes(direction)) return;
      // Now emit move to server
      try {
        const resp = await fetch(`/move?${direction}`);
        const moveResult = await resp.json();
        if (moveResult.success === false) throw new Error('Move failed');
      } catch (e) {
        console.error(`${e}\nMove failed.`);
      }
    },
    getData() {
      this.pollInterval = setInterval(async () => {
        try {
          const data = await fetch('/data?odom&move&dist');
          const dataResult = await data.json();
          this.odometer = parseFloat(dataResult.odom);
          this.moves = parseFloat(dataResult.move);
          this.sensor = parseFloat(dataResult.dist).toFixed(2);
          if (!this.id) this.id = dataResult.id;
          if (!this.created) this.id = dataResult.created;
        } catch (e) {
          console.error('Failed to fetch latest data.');
        }
      }, 1500);
    },
  },
  created() {
    this.getData();
  },
  beforeDestroy() {
    this.pollInterval = null;
  },
};
</script>

<style>
  .home {
    display: grid; grid-template-columns: repeat(3, 1fr);
    height: 100%; grid-template-rows: auto auto 1fr auto;
    grid-gap: 10px;
  }
  .title {
    grid-column: -1 / 1; text-align: center; margin: 0;
  }
</style>
