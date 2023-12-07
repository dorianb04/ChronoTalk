<template>
  <div>
    <div class="game-menu">
      <h1 class="title has-text-white has-text-centered">Welcome to Chronotalk</h1>
        
      <div class="cards-of-characters columns is-multiline is-centered is-marginless">
        <div v-for="character in characters" :key="character.id" class="column is-one-third">
          <router-link :to="{ name: 'GameTalk', params: { characterName: character.name } }">
            <!-- Wrap card content in a container -->
            <div class="card-container">
              <div class="card mx-4 my-4">
                <div>
                  
                </div>
                <div class="card-image">
                  <figure class="image is-4by3 m-6">
                    <img :src="character.image" alt="Character Image" class="myimage is-centered my-5"/>
                  </figure>
                </div>
                <div class="card-content">
                  <div class="media">
                    <div class="media-left">
                      <figure class="image is-48x48">
                        <img :src="character.image" alt="Character Image" class="myimage"/>
                      </figure>
                    </div>
                    <div class="media-content">
                      <p class="title is-4 has-text-white">{{ character.name }}</p>
                      <p class="subtitle is-6 has-text-white">{{ character.date }}</p>
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
      <h1 class="subtitle has-text-white has-text-centered">
        Please select your character
      </h1>
    </div>
  </div>
</template>
  
<script>
  import CharacterCard from "@/components/CharacterCard.vue";
  
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
            description: "Napoleon Bonaparte was a French military and political leader who played a key role in the Napoleonic Wars.",
          },
          {
            id: 2,
            name: "Julius Caesar",
            image: require("@/assets/unknown.jpg"),
            date: "Date of Birth: July 12 or 13, 100 BC",
            description: "Julius Caesar was a Roman general and statesman who played a crucial role in the end of the Roman Republic.",
          },
          {
            id: 3,
            name: "Harald Bluetooth",
            image: require("@/assets/unknown.jpg"),
            date: "Date of Birth: circa 910",
            description: "Harald Bluetooth was a Danish king known for introducing Christianity to Denmark.",
          },
        ],
        errors: [],
      };
    },
    components: {
      CharacterCard,
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
    border-radius: 50px; /* Add rounded border */
    background-color: #7070704d;
    color: #fff;
  }
</style>
  