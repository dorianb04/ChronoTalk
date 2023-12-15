<template>
  <div class="custom-audio-player">
    <button @click="togglePlay" class="play-button">
      <img :src="isPlaying ? pause : play" alt="Play/Pause Icon" />
    </button>
  </div>
</template>

<script>
import { faPlay, faPause } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

export default {
  data() {
    return {
      isPlaying: false,
      progress: 0,
      audio: null,
      play: null,
      pause: null,
      play: require("@/assets/play.png"),
      pause: require("@/assets/pause.png"),
    };
  },
  methods: {
    togglePlay() {
      if (this.isPlaying) {
        this.audio.pause();
      } else {
        this.audio.play();
      }
      this.isPlaying = !this.isPlaying;
    },
    updateProgress() {
      const currentTime = this.audio.currentTime;
      const duration = this.audio.duration;
      this.progress = (currentTime / duration) * 100 || 0;
    },
  },
  components: {
    FontAwesomeIcon,
  },
  mounted() {
    this.audio = new Audio();
    this.audio.src = this.src;
    this.audio.addEventListener("timeupdate", this.updateProgress);
    this.togglePlay();
  },
  props: {
    src: String,
  },
};
</script>

<style scoped>
.custom-audio-player {
  display: flex;
  align-items: center;
}

.play-button {
  /* Add your styling here */
  margin-top: 10px;
  background-color: #ffffff00;
  min-width: 25px;
  min-height: 25px;
  max-width: 40px;
  max-height: 40px;
  border: none;

  /* Add more styles as needed */
}

</style>