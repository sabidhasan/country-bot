<template>
  <div class="histogram">
    <canvas ref='canvas'></canvas>
    <label>{{ label }}</label>
  </div>
</template>

<script>
export default {
  name: 'Histogram',
  props: {
    data: { type: Array, required: true },
    label: { type: String, required: true },
  },
  data() {
    return {
      canvasElem: this.$refs.canvas,
    };
  },
  methods: {
    buildHistogram(data) {
      const { canvas } = this.$refs;
      canvas.width = data[0].length;
      canvas.height = data.length;

      const ctx = canvas.getContext('2d');
      const colors = {
        0: '#a33327', 1: '#ad8173',
      };

      for (const [i, row] of Object.entries(data)) {
        for (const [j, pixel] of Object.entries(row)) {
          ctx.fillStyle = colors[pixel];
          ctx.fillRect(j, i, 1, 1);
        }
      }
    },
  },
  mounted() {
    this.buildHistogram(this.data);
  },
  watch: {
    data(newData) {
      this.buildHistogram(newData);
    },
  },
};
</script>

<style>
.histogram {
  grid-column: 1 / -1; display: flex; align-items: center; justify-content: center;
  flex-direction: column;
}
</style>
