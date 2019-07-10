<template>
  <div class="car_stats">
    <span>Odometer</span>       <span>{{odomDist}}</span>
    <span>Moves</span>          <span>{{moves}}</span>
    <span>Forward Sensor</span> <span>{{sensorDist}}</span>
    <span>Created</span>        <span>{{createdDate}}</span>
    <span>Object ID</span>      <span>{{id || '-'}}</span>
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
    odomDist() {
      return `${this.odometer.toFixed(2)} cm`;
    },
    sensorDist() {
      return `${this.sensor.toFixed(2)} cm`;
    },
    createdDate() {
      if (!this.created) {
        return '-';
      }
      const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
      const date = new Date(this.created * 1000);

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
  display: grid; grid-template-columns: auto auto; color: var(--light);
  grid-template-rows: repeat(auto-fill, minmax(2rem, 1fr)); font-size: 1.3rem;
}
@media screen and (max-width: 500px) {
  .car_stats {
    grid-column: 1 / -1; grid-template-rows: repeat(auto-fill, 1.2rem); font-size: 1rem;
    margin: 0 5px;
  }
}
</style>
