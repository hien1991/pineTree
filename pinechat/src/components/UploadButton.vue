<template>
  <div class="upload-wrapper">
    <input type="file" ref="fileInput" @change="uploadFile" style="display: none" />
    <template v-if="!uploading">
      <button class="upload-button" @click="openFileChooser">
        <img src="@/assets/upload-icon.png" alt="Uploads Icon" />
      </button>
    </template>
    <template v-else>
      <div class="upload-status">
        <div class="spinner"></div>
        <div class="tooltip">{{ this.$refs.fileInput.files[0]?.name }}</div>
      </div>
    </template>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "UploadButton",
  data() {
    return {
      uploading: false,
    };
  },
  methods: {
    openFileChooser() {
      this.$refs.fileInput.click();
    },
    async uploadFile() {
      this.uploading = true;
      const formData = new FormData();
      formData.append('file', this.$refs.fileInput.files[0]);

      try {
        const response = await axios.post(`${this.$apiUrl}/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        this.$emit('upload-success');
        console.log(response.data);
      } catch (error) {
        console.error('Error uploading file:', error);
      } finally {
        this.uploading = false;
      }
    },
  },
};
</script>


<style scoped>
.upload-wrapper {
  display: flex;
  align-items: center;
  margin-left: 0.5rem;
  position: relative;
}

.upload-button {
  background-color: #6a7f7a;
  border: none;
  cursor: pointer;
  padding: 5px;
  border-radius: 4px;
  vertical-align: middle;
  transition: background-color 0.2s;
}

.upload-button:hover {
  background-color: #5a6f6a;
}

.upload-button img {
  width: 24px;
  height: 24px;
}

.upload-status {
  position: relative;
  width: 34px;
  height: 34px;
}

.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #6a7f7a;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  animation: spin 2s linear infinite;
}

.tooltip {
  visibility: hidden;
  background-color: #6a7f7a;
  color: #fff;
  text-align: center;
  padding: 5px;
  border-radius: 4px;
  position: absolute;
  z-index: 1;
  bottom: 125%;
  left: 50%;
  margin-left: -60px;
  width: 150px;
  opacity: 0;
  transition: opacity 0.3s;
}

.upload-status:hover .tooltip {
  visibility: visible;
  opacity: 1;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
