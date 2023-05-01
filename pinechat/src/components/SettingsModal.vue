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
      <label for="model-selection">Use GPT-4:</label>
      <input type="checkbox" id="model-selection" :checked="useGpt4Key" @input="onUseGpt4KeyChange"
        ref="modelSelection" />
      <button @click="saveKeys" :disabled="submitDisabled" class="save-button">Save</button>
      <button @click="$emit('close')">Close</button>
      <p :class="displayMessageClass">{{ displayMessage }}</p>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import axios from 'axios';

export default {
  name: "SettingsModal",
  data() {
    return {
      displayMessage: '',
      displayMessageClass: 'success-message',
      submitDisabled: false,
    };
  },
  computed: {
    ...mapGetters(["getPineconeApiKey", "getPineconeEnvKey", "getOpenaiApiKey", "getUseGpt4Key"]),
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
    useGpt4Key: {
      get() {
        return this.getUseGpt4Key;
      },
      set(value) {
        this.updateUseGpt4Key(value);
      },
    },
  },
  emits: ['close', 'api-keys-updated'],
  methods: {
    ...mapActions(["updatePineconeApiKey", "updatePineconeEnvKey", "updateOpenaiApiKey", "updateUseGpt4Key"]),
    saveKeys() {
      this.$emit("api-keys-updated");
      this.displayMessageClass = 'success-message';
      this.displayMessage = 'API keys saved successfully!';
      setTimeout(() => {
        this.displayMessage = '';
        this.$emit('close');
      }, 1500);
    },
    onUseGpt4KeyChange(event) {
      if (event.target.checked) {
        this.submitDisabled = true;
        this.displayMessageClass = 'success-message';
        this.displayMessage = 'Checking GPT-4 availability...';
        this.checkGpt4Access()
          .then((hasAccess) => {
            if (hasAccess) {
              this.updateUseGpt4Key(true);
              this.displayMessage = 'GPT-4 check confirmed.';
            } else {
              this.$refs.modelSelection.checked = false; //undo user checking the check-box
              this.displayMessageClass = 'error-message';
              this.displayMessage = "We're sorry, but it seems you don't have GPT-4 access.";
            }
          })
          .catch((error) => {
            console.error(error);
            this.displayMessage = 'An error occurred while checking GPT-4 access.';
          })
          .finally(() => {
            this.submitDisabled = false;
          });
      } else {
        this.updateUseGpt4Key(false);
        this.displayMessage = '';
      }
    },
    async checkGpt4Access() {
      const openaiApiKey = this.openaiApiKey;
      const model = 'gpt-4';

      return axios
        .get(`https://api.openai.com/v1/models/${model}`, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${openaiApiKey}`,
          },
        })
        .then((response) => {
          if (response.status === 200 && response.data && response.data.id === model) {
            return true;
          } else {
            return false;
          }
        })
        .catch((error) => {
          console.error(error);
          return false;
        });
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
  display: flex;
  justify-content: center;
  align-items: center;
}

.settings-modal-content {
  background-color: #fefefe;
  padding: 20px;
  border: 1px solid #888;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
  border-radius: 4px;
}

.settings-modal-content h2 {
  margin-top: 0;
  margin-bottom: 20px;
  text-align: center;
  font-size: 24px;
  font-weight: 600;
}

.settings-modal-content label {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 5px;
}

.settings-modal-content input[type="text"] {
  display: block;
  width: 100%;
  padding: 8px 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 15px;
  box-sizing: border-box;
}

.settings-modal-content .checkbox-container {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.settings-modal-content input[type="checkbox"] {
  margin: 0;
  width: 20px;
  height: 20px;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
  cursor: pointer;
  position: relative;
}

.settings-modal-content input[type="checkbox"]:checked {
  background-color: #3a3a3a;
}

.settings-modal-content input[type="checkbox"]:checked::after {
  content: "";
  display: block;
  position: absolute;
  width: 6px;
  height: 12px;
  border: solid #fff;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg) translateX(4px) translateY(1px);
}

.settings-modal-content button {
  background-color: #3a3a3a;
  color: white;
  border: none;
  font-size: 16px;
  padding: 8px 12px;
  border-radius: 4px;
  margin-top: 10px;
  margin-right: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.settings-modal-content button:hover {
  background-color: #4a4a4a;
}

.success-message {
  color: green;
  font-weight: bold;
  text-align: center;
  margin-top: 1rem;
}

.error-message {
  color: red;
  font-weight: bold;
  text-align: center;
  margin-top: 1rem;
}

.save-button {
  background-color: #3a3a3a;
  color: white;
  border: none;
  font-size: 16px;
  padding: 8px 12px;
  border-radius: 4px;
  margin-top: 10px;
  margin-right: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.save-button:hover:not(:disabled) {
  background-color: #4a4a4a;
}

.save-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
