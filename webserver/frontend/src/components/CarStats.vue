<template>
  <div class="car_stats">
    <span>Odometer</span>       <span>{{odometer.toFixed(2)}} cm</span>
    <span>Moves</span>          <span>{{moves}}</span>
    <span>Forward Sensor</span> <span>{{sensor}} cm</span>
    <span>Created</span>        <span>{{createdDate}}</span>
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
  computed: {
    createdDate: function () {
      const months = ["JAN", "FEB", "MAR","APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
      const date = new Date(this.created);
      
      const year = date.getFullYear();
      const month = months[date.getMonth()];
      const day = date.getDate();
      const hours = date.getHours();
      const minutes = date.getMinutes();
      const seconds = date.getSeconds();

      return `${day} ${month} ${year} at ${hours}:${minutes}:${seconds}`;
    },
  },
};
</script>

<style scoped>
.car_stats {
  display: grid; grid-template-columns: auto auto;
  grid-template-rows: repeat(auto-fill, minmax(2rem, 1fr));
}
@media screen and (max-width: 500px) {
  .car_stats {
    grid-column: 1 / -1;
  }
}
</style>
