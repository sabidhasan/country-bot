<template>
  <div class="car_view">
    <img src="http://192.168.50.241:4000/camera" class="car_view_img" alt="A view from the front of the car" />
    </div>
</template>

<script>
export default {
  name: 'CarView',
  props: {
  },
};
</script>

<style scoped>
.car_view {
  grid-column: 1 / span 2;
}
.car_view_img {
  max-width: 100%; max-height: 100%;
}
@media screen and (max-width: 500px) {
  .car_view {
    grid-column: 1 / -1;
  }
}
</style>
