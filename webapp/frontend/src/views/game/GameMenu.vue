<template>
  <div>
    <!-- Loader Section -->
    <div v-if="!modelLoaded" class="loader-container">
      <div class="lds-roller">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
      <p class="loading-text">Loading Model...</p>
    </div>

    <!-- Normal Page Section -->
    <div v-else>
      <div class="game-menu">
        <h1 class="title has-text-white has-text-centered">
          Welcome to Chronotalk
        </h1>

        <div
          class="cards-of-characters columns is-multiline is-centered is-marginless"
        >
          <div
            v-for="character in characters"
            :key="character.id"
            class="column is-one-third"
          >
            <router-link
              v-if="modelLoaded"
              :to="{
                name: 'GameTalk',
                params: { characterName: character.name },
              }"
            >
              <!-- Wrap card content in a container -->
              <div class="card-container">
                <div class="card mx-4 my-4">
                  <div></div>
                  <div class="card-image">
                    <figure class="image is-4by3 m-6">
                      <img
                        :src="character.image"
                        alt="Character Image"
                        class="myimage is-centered my-5"
                      />
                    </figure>
                  </div>
                  <div class="card-content">
                    <div class="media">
                      <div class="media-left">
                        <figure class="image is-48x48">
                          <img
                            :src="character.image"
                            alt="Character Image"
                            class="myimage"
                          />
                        </figure>
                      </div>
                      <div class="media-content">
                        <p class="title is-4 has-text-white">
                          {{ character.name }}
                        </p>
                        <p class="subtitle is-6 has-text-white">
                          {{ character.date }}
                        </p>
                      </div>
                    </div>
                    <div class="content">
                      {{ character.description }}
                    </div>
                  </div>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "GameMenu",
  data() {
    return {
      characters: [
        {
          id: 1,
          name: "Napoleon",
          image: require("@/assets/napoleon.jpg"),
          date: "Date of Birth: August 15, 1769",
          description:
            "Napoleon Bonaparte was a French military and political leader who played a key role in the Napoleonic Wars.",
        },
        {
          id: 2,
          name: "Julius Caesar",
          image: require("@/assets/unknown.jpg"),
          date: "Date of Birth: July 12 or 13, 100 BC",
          description:
            "Julius Caesar was a Roman general and statesman who played a crucial role in the end of the Roman Republic.",
        },
        {
          id: 3,
          name: "Harald Bluetooth",
          image: require("@/assets/unknown.jpg"),
          date: "Date of Birth: circa 910",
          description:
            "Harald Bluetooth was a Danish king known for introducing Christianity to Denmark.",
        },
      ],
      modelLoaded: false,
      errors: [],
    };
  },
  mounted() {
    this.loadModel();
  },
  methods: {
    loadModel() {
      axios
        .post(`/api/game/loadModel/`, {})
        .then((response) => {
          console.log(response.data);
          this.modelLoaded = true;
        })
        .catch((error) => {
          console.error("Failed to load model", error);
          this.errors.push("Failed to load model");
        });
    },
  },
};
</script>

<style lang="scss">
@import "../../../node_modules/bulma";

/* Add any specific styles for the GameMenu component here if needed */
.cards-of-characters {
  margin-top: 20px;
  color: #fff;
}

.card-container {
  display: flex;
  flex-direction: column;
  height: 75vh;
  color: #fff;
}

.myimage {
  border-radius: 50px;
}

.card {
  border-radius: 50px;
  background-color: #7070704d;
  color: #fff;
}

.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  color: #fff;
}

.loading-text {
  margin-top: 10px;
}
.lds-roller {
  display: inline-block;
  position: relative;
  width: 80px;
  height: 80px;
}
.lds-roller div {
  animation: lds-roller 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
  transform-origin: 40px 40px;
}
.lds-roller div:after {
  content: " ";
  display: block;
  position: absolute;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  margin: -4px 0 0 -4px;
}


.lds-roller div:nth-child(1) {
  animation-delay: -0.036s;
}

.lds-roller div:nth-child(1):after {
  top: 63px;
  left: 63px;
}
.lds-roller div:nth-child(2) {
  animation-delay: -0.072s;
}
.lds-roller div:nth-child(2):after {
  top: 68px;
  left: 56px;
}
.lds-roller div:nth-child(3) {
  animation-delay: -0.108s;
}
.lds-roller div:nth-child(3):after {
  top: 71px;
  left: 48px;
}
.lds-roller div:nth-child(4) {
  animation-delay: -0.144s;
}
.lds-roller div:nth-child(4):after {
  top: 72px;
  left: 40px;
}
.lds-roller div:nth-child(5) {
  animation-delay: -0.18s;
}
.lds-roller div:nth-child(5):after {
  top: 71px;
  left: 32px;
}
.lds-roller div:nth-child(6) {
  animation-delay: -0.216s;
}
.lds-roller div:nth-child(6):after {
  top: 68px;
  left: 24px;
}
.lds-roller div:nth-child(7) {
  animation-delay: -0.252s;
}
.lds-roller div:nth-child(7):after {
  top: 63px;
  left: 17px;
}
.lds-roller div:nth-child(8) {
  animation-delay: -0.288s;
}
.lds-roller div:nth-child(8):after {
  top: 56px;
  left: 12px;
}
@keyframes lds-roller {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}



@keyframes colorChange {
  0% { background: #ff0000; }
  20% { background: #ff7f00; } 
  40% { background: #ffff00; } 
  60% { background: #00ff00; } 
  80% { background: #0000ff; }
  100% { background: #ff0000; }
}

.lds-roller div:after {
  animation: lds-roller 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite, colorChange 1.2s linear infinite;
}

.lds-roller div:nth-child(1):after {
  animation-delay: -0.036s;
}

.lds-roller div:nth-child(2):after {
  animation-delay: -0.072s;
}

.lds-roller div:nth-child(3):after {
  animation-delay: -0.108s;
}

.lds-roller div:nth-child(4):after {
  animation-delay: -0.144s;
}

.lds-roller div:nth-child(5):after {
  animation-delay: -0.18s;
}

.lds-roller div:nth-child(6):after {
  animation-delay: -0.216s;
}

.lds-roller div:nth-child(7):after {
  animation-delay: -0.252s;
}

.lds-roller div:nth-child(8):after {
  animation-delay: -0.288s;
}
</style>