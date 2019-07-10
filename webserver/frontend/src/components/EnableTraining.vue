<template>
  <div class="enable_training">
    <button @click="startRecording" :disabled="recording">
      <span v-html="recordingSymbol"></span>
      {{ recordingCommand }}
    </button>
    <div class="training_state">
      {{ recordingState }} <br />
      Last data recorded - {{ lastTrainingRecorded }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'EnableTraining',
  data() {
    return {
      recording: false,
    };
  },
  props: [
    'lastTrainingRecorded',
  ],
  methods: {
    async startRecording() {
      try {
        const resp = await fetch('/enable_training');
        const trainingResult = await resp.json();
        this.recording = trainingResult.training;
      } catch (e) {
        alert('Could not set training mode.');
      }
    },
  },
  computed: {
    recordingSymbol() {
      return this.recording ? '||' : '&#11044;';
    },
    recordingCommand() {
      return this.recording ? 'Recording...' : 'Start Recording';
    },
    recordingState() {
      return this.recording ? 'Recording Data' : 'Not recording';
    },
  },
};
</script>

<style scoped>
.enable_training {
  display: flex; flex-direction: column; justify-content: space-evenly; align-items: center;
}
button {
  align-self: center; justify-self: center; padding: 20px; border-radius: 3px; color: var(--dark);
  border: 3px solid var(--accent-dark); background: var(--accent-light); font-size: 1.2em;
}
button span {
  display: block; font-size: 2rem;
}
.training_state {
  font-weight: bold; font-size: 1.3rem; color: var(--light); text-align: center;
}
@media screen and (max-width: 500px) {
  .enable_training {
    grid-column: 1 / -1;
  }
  button {
    font-size: 1rem; padding: 10px 35px;
  }
  button span {
    display: none;
  }
  .training_state {
    display: none;
  }
}
</style>
