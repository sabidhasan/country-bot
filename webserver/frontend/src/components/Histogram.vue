<template>
  <div>
    <canvas ref='canvas'></canvas>
    </div>
</template>

<script>
export default {
  name: 'Histogram',
  props: {
    'data': { type: Array, required: true }
  },
  data() {
    return {
      canvasElem: this.$refs.canvas
    }
  },
  watch: {
    data: function(newData, oldData) {
      const canvas = this.$refs.canvas;
      canvas.width = newData[0].length;
      canvas.height = newData.length;

      const ctx = canvas.getContext('2d');
      const colors = {
        0: '#ff0000', 1: '#00ffff'
      };

      for (let [i, row] of Object.entries(newData)) {
        for (let [j, data] of Object.entries(row)) {

          ctx.fillStyle = colors[data];
          ctx.fillRect(j,i,1,1);
        }
      }
    }
  }
}
</script>

<style>

</style>