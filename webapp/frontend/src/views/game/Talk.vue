<template>
  <div class="talk-page">
    <div class="talk-container">
      <div class="character-photo">
        <img :src="characterImage" alt="Character Photo" />
      </div>

      <div class="dialogue-container">
        <div class="dialogue-bubble" ref="dialogueBubble">
          <div v-for="(message, index) in conversation" :key="index" class="message-container">
            <div v-if="message.type === 'character'" class="character-message">
              <p v-html="message.text"></p>
            </div>
            <div v-else class="user-message">
              <p v-html="message.text"></p>
            </div>
          </div>
        </div>

        <div class="user-input">
          <textarea v-model="userMessage" @keydown.enter="sendMessage" :disabled="isInputDisabled" placeholder="Type your message..."></textarea>
          <!--class="button is-medium is-rounded has-text-weight-bold"--><button class="button-85" @click="sendMessage" :disabled="userMessage.trim().length === 0">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>
  
  
<script>
import axios from 'axios'
export default {
  data() {
    return {
      characterName: this.$route.params.characterName,
      characterImage: this.loadCharacterImage(),
      characterDialogue: "Loading...",
      userMessage: "",
      isInputDisabled: false,
      conversation: [],
    };
  },
  mounted() {
    this.getCharacterDialogue();
  },
  methods: {
    getCharacterDialogue() {
      axios
        .get(`/api/game/getFirstMessage`, { params: { characterName: this.characterName } })
        .then((response) => {
          this.characterDialogue = response.data.CHAR_response;
          this.addToConversation(response.data.CHAR_response, 'character');
        })
        .catch((error) => {
          console.error('Error fetching character dialogue:', error);
          this.characterDialogue = "Sorry, I can't talk right now.";
          this.addToConversation(this.characterDialogue, 'character');
        });
    },
    sendMessage() {
      this.isInputDisabled = true;
      const requestData = {
        characterName: this.characterName,
        message: this.userMessage,
      };
      this.addToConversation(this.userMessage, 'user');
      // Scroll to the bottom after adding a new message
      this.$nextTick(() => {
        this.scrollToBottom();
      });
      axios
        .post("/api/game/postMessage/", requestData)
        .then((response) => {
          this.addToConversation(response.data.CHAR_response, 'character');
          this.userMessage = "";
          this.characterDialogue = response.data.CHAR_response;
          this.isInputDisabled = false;
          // Scroll to the bottom after adding a new message
          this.$nextTick(() => {
            this.scrollToBottom();
          });
        })
        .catch((error) => {
          if (error.response) {
            console.log(error.response);
          } else if (error.message) {
            console.log(JSON.stringify(error.message));
          } else {
            console.log(JSON.stringify(error));
          }
        });
    },
    scrollToBottom() {
      const dialogueBubble = this.$refs.dialogueBubble;
      dialogueBubble.scrollTop = dialogueBubble.scrollHeight;
    },
    addToConversation(text, type) {
      this.conversation.push({ text, type });
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
  margin-left: 20px;
  margin-right: 20px;
  display: flex;
  flex-direction: column;
  height: 87vh;
}

.talk-container {
  display: flex;
  flex: 1;
  align-items: stretch;
  margin-top: 20px;
  position: relative;
}

.character-photo {
  flex: 1;
}

.character-photo img {
  width: 100%;
  border-radius: 50%;
}

.dialogue-container {
  flex: 2;
  display: flex;
  flex-direction: column;
  margin-left: 10px;
  position: relative;
  background-color: #7070704d;
  border-radius: 10px;
  max-width: 100vh;
}

.dialogue-bubble {
  overflow-y: auto;
  max-height: 80vh;
  display: flex;
  flex-direction: column;/* Stack messages from bottom to top */
  padding: 25px 10px
}

.message-container {
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  
}

.character-message {
  padding: 10px 20px;
  border-radius: 10px;
  margin: 5px;
  background: linear-gradient(86deg, rgba(9,49,105,1) 35%, rgba(19,55,106,1) 100%);
  color: #fff;
  align-self: flex-start; /* Align character messages to the left */
  max-width: 70vh;
  word-wrap: break-word;
}

.user-message {
  padding: 10px 20px;
  border-radius: 10px;
  margin: 5px;
  background: linear-gradient(86deg, rgba(70,184,83,1) 0%, rgba(98,182,116,1) 100%);
  color: #fff;
  align-self: flex-end; /* Align user messages to the right */
  max-width: 70vh;
  word-wrap: break-word;
}



.user-input {
  margin-top: 20px;
  padding: 10px;
  display: flex;
  align-items: center;
  position: absolute; /* Position the user input absolutely */
  bottom: 0; /* Place the user input at the bottom */
  left: 0;
  right: 0;
}

textarea {
  flex: 1;
  padding: 10px;
  border: 1px solid #413f3f;
  border-radius: 10px;
  background-color: #7070704d;
  color: #fff;
}

textarea::placeholder {
  color: #fff;
}

textarea:focus { 
  outline: none !important;
}

button {
  margin-left: 10px;
  background-color: #5f5c5c;
  color: #fff;
  border-color: #5e5a5a;
}


/* CSS */
.button-85 {
  padding: 0.6em 2em;
  border: none;
  outline: none;
  color: rgb(255, 255, 255);
  background: #111;
  cursor: pointer;
  position: relative;
  z-index: 0;
  border-radius: 10px;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
}

.button-85:before {
  content: "";
  background: linear-gradient(
    45deg,
    #ff0000,
    #ff7300,
    #fffb00,
    #48ff00,
    #00ffd5,
    #002bff,
    #7a00ff,
    #ff00c8,
    #ff0000
  );
  position: absolute;
  top: -2px;
  left: -2px;
  background-size: 400%;
  z-index: -1;
  filter: blur(5px);
  -webkit-filter: blur(5px);
  width: calc(100% + 4px);
  height: calc(100% + 4px);
  animation: glowing-button-85 20s linear infinite;
  transition: opacity 0.3s ease-in-out;
  border-radius: 10px;
}

@keyframes glowing-button-85 {
  0% {
    background-position: 0 0;
  }
  50% {
    background-position: 400% 0;
  }
  100% {
    background-position: 0 0;
  }
}

.button-85:after {
  z-index: -1;
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  background: #222;
  left: 0;
  top: 0;
  border-radius: 10px;
}
.dialogue-bubble::-webkit-scrollbar {
  width: 8px; /* Set the width of the scrollbar */
}

.dialogue-bubble::-webkit-scrollbar-thumb {
  background-color: #6b6b6b; /* Set the color of the scrollbar thumb */
  border-radius: 4px; /* Set the border-radius of the scrollbar thumb */
}

.dialogue-bubble::-webkit-scrollbar-track {
  background-color: #7070704d; /* Set the color of the scrollbar track */
}

.dialogue-bubble::-webkit-scrollbar-thumb:hover {
  background-color: #555; /* Set the color of the scrollbar thumb on hover */
}


</style>