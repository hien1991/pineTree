<template>
  <div class="upload-wrapper">
    <input type="file" ref="fileInput" @change="uploadFile" style="display: none"/>
    <button class="upload-button" @click="openFileChooser">
      <img src="@/assets/upload-icon.png" alt="Uploads Icon"/>
    </button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "UploadButton",
  methods: {
    openFileChooser() {
      this.$refs.fileInput.click();
    },
    async uploadFile() {
      const formData = new FormData();
      formData.append('file', this.$refs.fileInput.files[0]);

      try {
        const response = await axios.post(`${this.$apiUrl}/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log(response.data);
      } catch (error) {
        console.error('Error uploading file:', error);
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
</style>
