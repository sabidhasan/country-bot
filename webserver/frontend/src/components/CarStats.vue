<template>
  <div class="car_stats">
    <span>Odometer</span>       <span>{{odometer}}m c</span>
    <span>Moves</span>          <span>{{sensor}}</span>
    <span>Forward Sensor</span> <span>{{moves}} cm</span>
    <span>Created</span>        <span>{{created}}</span>
    <span>Object ID</span>      <span>{{id}}</span>
  </div>
</template>

<script>
export default {
  name: 'CarStats',
  props: {
    odometer: { type: Number },
    moves: { type: Number },
    sensor: { type: Number },
    created: { type: Number },
    id: { type: Number },
  },
};
</script>

<style scoped>
.car_stats {
  display: grid; grid-template-columns: auto auto;
  grid-template-rows: repeat(auto-fill, minmax(2rem, 1fr));
}
</style>
