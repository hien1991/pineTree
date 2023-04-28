<template>
  <div class="settings-modal">
    <div class="settings-modal-content">
      <h2>Settings</h2>
      <label for="openai-api-key">OpenAI API Key:</label>
      <input type="text" id="openai-api-key" v-model="openaiApiKey" />
      <label for="pinecone-api-key">Pinecone API Key:</label>
      <input type="text" id="pinecone-api-key" v-model="pineconeApiKey" />
      <label for="pinecone-api-key">Pinecone env:</label>
      <input type="text" id="pinecone-env-key" v-model="pineconeEnvKey" />
      <button @click="saveKeys">Save</button>
      <button @click="$emit('close')">Close</button>
      <p class="success-message">{{ successMessage }}</p>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "SettingsModal",
  data() {
    return {
      successMessage: '',
    };
  },
  computed: {
    ...mapGetters(["getPineconeApiKey", "getPineconeEnvKey", "getOpenaiApiKey"]),
    pineconeApiKey: {
      get() {
        return this.getPineconeApiKey;
      },
      set(value) {
        this.updatePineconeApiKey(value);
      },
    },
    pineconeEnvKey: {
      get() {
        return this.getPineconeEnvKey;
      },
      set(value) {
        this.updatePineconeEnvKey(value);
      },
    },
    openaiApiKey: {
      get() {
        return this.getOpenaiApiKey;
      },
      set(value) {
        this.updateOpenaiApiKey(value);
      },
    },
  },
  emits: ['close'],
  methods: {
    ...mapActions(["updatePineconeApiKey", "updatePineconeEnvKey", "updateOpenaiApiKey"]),
    saveKeys() {
      this.$emit("api-keys-updated");
      this.showSuccessMessage(); //Shows success message for 1.5 seconds
      setTimeout(() => {
        this.$emit('close');
      }, 1500);
    },
    showSuccessMessage() {
      this.successMessage = 'API keys saved successfully!';
      setTimeout(() => {
        this.successMessage = '';
      }, 1500);
    },
  },
};
</script>

<style scoped>
.settings-modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.settings-modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.settings-modal-content h2 {
  margin-top: 0;
}

.settings-modal-content label,
.settings-modal-content input {
  display: block;
  margin-bottom: 10px;
}

.settings-modal-content button {
  background-color: #3a3a3a;
  color: white;
  border: none;
  font-size: 16px;
  padding: 5px 10px;
  margin-top: 10px;
  margin-right: 10px;
  cursor: pointer;
}

.success-message {
  color: green;
  font-weight: bold;
  text-align: center;
  margin-top: 1rem;
}
</style>
