<template>
  <div class="chat-container">
    <div class="chat-header">
      <h1>PineChat</h1>
    </div>
    <div class="chat-window">
      <div class="chat-messages" ref="chatMessages">
        <div class="spacer"></div>
        <div v-for="(message, index) in getChatMessages.slice().reverse()" :key="index" class="message"
          :class="message.type">
          <div class="message-bubble">{{ message.text }}</div>
          <TypingLoader v-if="isTyping && index === 0" />
        </div>
      </div>
      <button class="scroll-down" @click="scrollToBottom">↓</button>
    </div>
    <div class="input-area">
      <ChatInput ref="chatInputComponent" class="chat-input-component" @send="submitMessage" :is-submitting="isTyping" />
      <UploadButton />
    </div>
    <div class="db-results-wrapper" :style="{ display: dbResultsVisible ? 'block' : 'none' }">
      <DbResults v-if="dbResultsVisible" :results="searchResults" :searchQueryDisplay="searchQueryDisplay" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import DbResults from './common/DbResults.vue';
import UploadButton from './UploadButton.vue';
import ChatInput from './common/ChatInput.vue';
import TypingLoader from './common/TypingLoader.vue';
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'ChatWindow',
  components: {
    DbResults,
    UploadButton,
    TypingLoader,
    ChatInput,
  },
  data() {
    return {
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
  computed: {
    ...mapGetters(['getChatMessages']),
  },
  methods: {
    ...mapActions(['addChatMessage']),
    scrollToBottom() {
      this.$nextTick(() => {
        let scrollHeight = this.$refs.chatMessages.scrollHeight
        window.scrollTo(0, scrollHeight)
      })
    },
    async submitMessage(message) {
      if (!message.trim()) return;
      this.addChatMessage({ type: 'user', text: message });
      this.isTyping = true;

      try {
        const response = await axios.post(`${this.$apiUrl}/chat`, { input_text: message });

        if (response.data.status === 'error') {
          this.addChatMessage({ type: 'error', text: response.data.message });
        } else {
          const aiResponse = response.data.response;
          this.searchResults = response.data.search_results; //Sent to DbResults.vue
          this.searchQueryDisplay = response.data.db_query;

          const chatResponse = aiResponse;
          this.addChatMessage({ type: 'bot', text: chatResponse });
        }
      } catch (error) {
        console.error(error);
        this.addChatMessage({ type: 'error', text: 'An error occurred while sending your message.' });
      } finally {
        this.isTyping = false;
        this.$nextTick(() => {
          this.$refs.chatInputComponent.reset();
        });
      }
    },
  }
};
</script>

<style scoped>
.input-area {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  bottom: 1%;
  padding-right: 1rem;
  box-sizing: border-box;
  width: 800px;
  border-top: 2px solid #70877F;
  background-color: #3c6e71;
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
  border-bottom-left-radius: 15px;
  border-bottom-right-radius: 15px;
  box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.1);
}

@media screen and (max-width: 800px) {
  .input-area {
    width: 85vw;
  }
}

.chat-input-component {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 90%;
  max-width: 800px;
}

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

.error {
  font-size: 1.1rem;
  color: #d9534f;
  text-align: left;
}

.error .message-bubble {
  background-color: #f9d9d7;
  color: #d9534f;
  border: 1px solid #d8a6a4;
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