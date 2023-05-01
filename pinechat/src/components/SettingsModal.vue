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
      <label class="model-toggle-container">GPT-4:
        <div class="switch">
          <input type="checkbox" id="model-selection" :checked="useGpt4Key" @input="onUseGpt4KeyChange"
            ref="modelSelection" />
          <span class="slider round"></span>
        </div>
      </label>
      <button @click="saveKeys" :disabled="submitDisabled" class="save-button">Save</button>
      <button @click="$emit('close')" class="close-button">Close</button>
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
}

.settings-modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 400px;
}

.settings-modal-content h2 {
  margin-top: 0;
}

.settings-modal-content label,
.settings-modal-content input {
  display: block;
  margin-bottom: 10px;
  width: 90%;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 28px;
  margin-bottom: -1.5%;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
  border-radius: 28px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 1px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
  border-radius: 50%;
}

.switch input:checked+.slider {
  background-color: #2196F3;
}

.switch input:focus+.slider {
  box-shadow: 0 0 1px #2196F3;
}

.switch input:checked+.slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
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
  padding: 5px 10px;
  margin-top: 10px;
  margin-right: 10px;
  cursor: pointer;
}

.save-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}</style>
