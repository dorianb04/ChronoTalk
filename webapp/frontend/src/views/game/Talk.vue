<template>
    <div class="talk-page">
        <h1 class="title has-text-centered">Talk with {{ characterName }}</h1>

        <div class="talk-container">
            <div class="character-photo">
                <img :src="characterImage" alt="Character Photo" />
            </div>

            <div class="dialogue-bubble">
                {{ characterDialogue }}
            </div>
        </div>

        <div class="user-input">
            <textarea
                v-model="userMessage"
                @keydown.enter="sendMessage"
                :disabled="isInputDisabled"
                placeholder="Type your message..."
            ></textarea>
            <button class="button is-medium is-rounded has-text-weight-bold" @click="sendMessage">Send</button>
        </div>

        <router-link to="/game/game-menu" class="button is-small is-outlined is-rounded is-fixed-bottom my-4 has-text-weight-bold">
        Back
        </router-link>
    </div>
</template>
  
  
<script>
import axios from 'axios'
export default {
  data() {
    return {
      characterName: this.$route.params.characterName,
      characterImage: this.loadCharacterImage(),
      characterDialogue: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
      userMessage: "",
      isInputDisabled: false,
    };
  },
  methods: {
    sendMessage() {
      this.isInputDisabled = true;
      const requestData = {
        characterName: this.characterName,
        message: this.userMessage,
      };
      this.userMessage = "";
      axios
          .post("/api/game/postMessage/", requestData)
          .then(response => {
               // Log MP4_path and CHAR_response to the console
              console.log('MP4_path:', response.data.MP4_path);
              console.log('CHAR_response:', response.data.CHAR_response);

              // Update your Vue component state or perform other actions if needed
              // ...
              this.userMessage = "";
              this.isInputDisabled = false;
          })
          .catch(error => {
              if (error.response) {
                  for (const property in error.response.data) {
                      this.errors.push(`${property}: ${error.response.data[property]}`)
                  }

                  console.log(JSON.stringify(error.response.data))
              } else if (error.message) {
                  console.log(JSON.stringify(error.message))
              } else {
                  console.log(JSON.stringify(error))
              }
          })
    },
    loadCharacterImage() {
      try {
        return require(`@/assets/${this.$route.params.characterName.toLowerCase()}.jpg`);
      } catch (error) {
        return require('@/assets/unknown.jpg');
      }
    },
  },
};
</script>

  
<style scoped>
.talk-page {
  margin: 20px;
}

.talk-container {
  display: flex;
  align-items: center;
  margin-top: 20px;
}

.character-photo {
  flex: 1;
}

.character-photo img {
  width: 100%;
  border-radius: 50%;
}

.dialogue-bubble {
  flex: 2;
  background-color: #e0e0e0;
  padding: 10px;
  border-radius: 10px;
  margin-left: 10px;
}

.user-input {
  margin-top: 20px;
  display: flex;
  align-items: center;
}

textarea {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  margin-left: 10px;
}
</style>

  