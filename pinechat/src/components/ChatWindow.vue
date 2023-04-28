<template>
  <div class="chat-container">
    <div class="chat-header">
      <h1>PineChat</h1>
    </div>
    <div v-if="isTyping" class="typing-indicator">
      <span class="dot"></span>
      <span class="dot"></span>
      <span class="dot"></span>
    </div>
    <div class="chat-window">
      <!-- Main chat area -->
      <div class="chat-messages" ref="chatMessages">
        <div class="spacer"></div>
        <div v-for="(message, index) in messages.slice().reverse()" :key="index" :class="message.type" class="message">
          <div class="message-bubble">{{ message.text }}</div>
        </div>
      </div>
      <button class="scroll-down" @click="scrollToBottom">↓</button>
    </div>
    <div class="chat-input">
      <!-- <input type="text" v-model="inputText" @keyup.enter="submitMessage" @input="resizeInput" @keydown="handleKeyDown" /> -->
      <textarea v-model="inputText" @keydown.enter.exact.prevent="submitMessage"
        @keydown.shift.enter.exact="handleKeyDown" @input="resizeInput" :style="{ resize: 'none', overflow: 'hidden' }"
        class="chat-input-field"></textarea>
      <button @click="submitMessage">Send</button>
      <UploadButton />
    </div>
    <div class="db-results-wrapper" :style="{ display: dbResultsVisible ? 'block' : 'none' }">
      <DbResults v-if="dbResultsVisible" :results="searchResults" :searchQueryDisplay="searchQueryDisplay" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import DbResults from './DbResults.vue';
import UploadButton from './UploadButton.vue';

export default {
  name: 'ChatWindow',
  components: {
    DbResults,
    UploadButton,
  },
  data() {
    return {
      inputText: "",
      messages: [],
      isTyping: false,
      searchResults: [],
      searchQueryDisplay: ''
    };
  },
  props: {
    dbResultsVisible: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    scrollToBottom() {
      this.$nextTick(() => {
        let scrollHeight = this.$refs.chatMessages.scrollHeight
        window.scrollTo(0, scrollHeight)
      })
    },
    async submitMessage() {
      if (!this.inputText.trim()) return;
      this.messages.push({ type: 'user', text: this.inputText });
      this.isTyping = true;
      try {
        axios.post(`${this.$apiUrl}/chat`, { input_text: this.inputText }).then((response) => {
          console.log(response.data);
          const aiResponse = response.data.response;
          this.searchResults = response.data.search_results; //Received by DatabaseResults.vue
          this.searchQueryDisplay = response.data.db_query;

          const chatResponse = aiResponse
          this.messages.push({ type: 'bot', text: chatResponse });
          this.isTyping = false;
        });
      } catch (error) {
        console.error('Error while communicating with chatbot:', error);
        this.messages.push({ type: 'error', text: 'Error while communicating with chatbot' });
        this.isTyping = false;
      }
      this.inputText = '';
    },
    //Below methods are for auto-sizing the input text field
    handleKeyDown(event) {
      if (event.key === "Enter" && event.shiftKey) {
        event.preventDefault();
        this.inputText += "\n";
      }
    },
    resizeInput(event) {
      const target = event.target;
      target.style.height = "auto";
      const maxHeight = 100; // Set the maximum height in pixels

      if (target.scrollHeight <= maxHeight) {
        target.style.height = `${target.scrollHeight}px`;
      } else {
        target.style.height = `${maxHeight}px`;
        target.style.overflowY = "scroll";
      }
      if (target.value === "") {
        target.style.height = "auto";
      }
    }

  }
};
</script>

<style scoped>
.chat-container {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  height: 100%;
  font-family: "Roboto", sans-serif;
}

.chat-window {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.chat-messages {
  padding-bottom: 110px;
  flex-grow: 1;
  overflow-y: auto;
  padding: 1rem;
  background-color: #f4f1ea;
  background-image: none;
  background-size: 8px 8px;
  display: flex;
  flex-direction: column-reverse;
}

.chat-header {
  background-color: olivedrab;
  color: white;
  padding: 10px;
  text-align: center;
  font-size: 24px;
}

.user {
  font-size: 1.1rem;
  color: #3c6e71;
  text-align: right;
}

.bot {
  font-size: 1.1rem;
  color: #284b5a;
}

.typing-indicator {
  display: flex;
  justify-content: center;
  margin-bottom: 5px;
  margin-top: 5px;
}

.dot {
  background-color: #8e9775;
  border-radius: 50%;
  width: 8px;
  height: 8px;
  margin: 0 2px;
  opacity: 0;
  animation: typingIndicator 1.2s infinite;
}

.message-bubble {
  display: inline-block;
  padding: 10px 15px;
  border-radius: 15px;
  margin: 5px;
  white-space: pre-wrap;
  max-width: 70%;
  /* Controls line breaks */
}

.user .message-bubble {
  background-color: #e0ede3;
  color: #333;
  border: 1px solid #c9d8c5;
}

.bot .message-bubble {
  background-color: #8e9775;
  color: #e6e6e6;
}

.chat-input {
  position: fixed;
  bottom: 0.5%;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 800px;
  display: flex;
  padding: 1rem;
  background-color: #3c6e71;
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
  border-bottom-left-radius: 15px;
  border-bottom-right-radius: 15px;
  box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.1);
}

.chat-input .chat-input-field {
  flex-grow: 1;
  margin-right: 0.5rem;
  padding: 5px;
  border: 1px solid #dcd9d5;
  border-radius: 4px;
  resize: none;
  overflow: hidden;
  min-height: 20px;
}

.chat-input button {
  background-color: #8e9775;
  color: #ffffff;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.chat-input button:hover {
  background-color: #7d8563;
}

.scroll-down {
  position: fixed;
  right: 1%;
  bottom: 13%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #8e9775;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.scroll-down:hover {
  background-color: #7d8563;
}

.spacer {
  height: 110px;
}
</style>
