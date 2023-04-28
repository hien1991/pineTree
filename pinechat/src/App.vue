<template>
  <div id="app">
    <nav class="top-nav">
      <button @click="toggleDbResults">Show Datababase Returns</button>
      <button @click="showSettings">Settings</button>
    </nav>
    <SideChatBar />
    <ChatWindow :dbResultsVisible="dbResultsVisible" />
    <SettingsModal v-if="settingsVisible" @close="showSettings" @api-keys-updated="initializeBackend" />
  </div>
  <div v-if="showGuideModal" class="guide-modal">
    <div class="guide-modal-content">
      <h2>Welcome to PineChat!</h2>
      <p>Before you can start using the app, please enter the required API keys in the settings.</p>
      <button @click="hideGuideModalAndShowSettings">Go to Settings</button>
    </div>
  </div>
</template>

<script>
import SettingsModal from "./components/SettingsModal.vue";
import ChatWindow from './components/ChatWindow.vue';
import SideChatBar from './components/SideChatBar.vue';
import axios from 'axios';

export default {
  name: "App",
  components: {
    ChatWindow,
    SideChatBar,
    SettingsModal,
  },
  data() {
    return {
      settingsVisible: false,
      showGuideModal: false,
      dbResultsVisible: false,
    };
  },
  methods: {
    showSettings() {
      this.settingsVisible = !this.settingsVisible;
    },
    toggleDbResults() {
      this.dbResultsVisible = !this.dbResultsVisible;
    },
    hideGuideModalAndShowSettings() {
      this.showGuideModal = false;
      this.showSettings();
    },
    initializeBackend() {
      const openaiApiKey = localStorage.getItem("openaiApiKey");
      const pineconeApiKey = localStorage.getItem("pineconeApiKey");
      const pineconeEnvKey = localStorage.getItem("pineconeEnvKey");

      if (openaiApiKey && pineconeApiKey && pineconeEnvKey) {
        axios.post(`${this.$apiUrl}/initialize`, {
          openaiApiKey,
          pineconeApiKey,
          pineconeEnvKey,
        });
      }
    },
  },
  mounted() {
    this.initializeBackend();

    const openaiApiKey = localStorage.getItem("openaiApiKey");
    const pineconeApiKey = localStorage.getItem("pineconeApiKey");
    const pineconeEnvKey = localStorage.getItem("pineconeEnvKey");

    if (!openaiApiKey || !pineconeApiKey || !pineconeEnvKey) {
      this.showGuideModal = true;
    }
  },
};
</script>

<style>
/* Global styles for the application */
/* More background patterns: https://www.toptal.com/designers/subtlepatterns/ */
body {
  font-family: 'Roboto', sans-serif;
  background-color: #f4f4f4;
  background-image: url(~@/assets/leaves.png);
  background-attachment: fixed;
}

.top-nav {
  display: flex;
  justify-content: flex-end;
  background-color: #3a3a3a;
  padding: 10px;
}

.top-nav button {
  background-color: #3a3a3a;
  color: white;
  border: none;
  font-size: 16px;
  margin-left: 10px;
  cursor: pointer;
  border-radius: 4px;
  padding: 5px 10px;
  transition: background-color 0.3s;
}

.top-nav button:hover {
  background-color: #6b8e23;
}

.guide-modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
}

.guide-modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}

.guide-modal-content h2 {
  color: #6b8e23;
}

.guide-modal-content button {
  background-color: #6b8e23;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 20px;
  border-radius: 3px;
  transition: background-color 0.3s;
}

.guide-modal-content button:hover {
  background-color: #3a3a3a;
}
</style>
