<template>
  <div class="pinedocs">
    <div class="header">
      <button @click="openUploadModal">Upload</button>
      <button @click="handleNewDoc">New Doc</button>
    </div>
    <div class="file-grid">
      <div v-for="file in files" :key="file.id" class="file-card" @click="handleSelect(file.id)">
        <div class="file-info">
          <h3>{{ file.name }}</h3>
          <p>Uploaded: {{ file.uploadedDate }}</p>
          <p>Size: {{ file.size }}</p>
          <p>Chunks: {{ file.chunks }}</p>
        </div>
        <div class="file-options">
          <button @click.stop="handleOptions(file.id)">Options</button>
        </div>
      </div>
    </div>
    <div class="chat-input">
      <input v-model="chatInput" @keyup.enter="handleSend" type="text" placeholder="Ask about selected documents" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'PineDocs',
  data() {
    return {
      files: [], // Replace with actual files fetched from your database
      selectedFiles: [],
      chatInput: '',
    };
  },
  methods: {
    async fetchFiles() {
      try {
        const response = await fetch(`${this.$apiUrl}/get_all_uploads`);
        const uploadedFiles = await response.json();
        this.files = uploadedFiles.map((file) => ({
          id: file.memory_id,
          name: file.filename,
          uploadedDate: file.timestamp,
          size: file.file_size,
          chunks: file.num_chunks,
        }));
        console.log(uploadedFiles)
      } catch (error) {
        console.error('Error fetching uploaded files:', error);
      }
    },
    handleSelect(fileId) {
      const index = this.selectedFiles.indexOf(fileId);
      if (index === -1) {
        this.selectedFiles.push(fileId);
      } else {
        this.selectedFiles.splice(index, 1);
      }
    },
    handleOptions(/*fileId*/) {
      // Handle options like renaming and deleting the file
      // You can open a modal with the options or use any other preferred method
    },
    openUploadModal() {
      // Open a modal for file upload with progress indicator
    },
    handleUpload() {
      // Handle file upload and update this.files with the new file
    },
    handleNewDoc() {
      // Transition to a separate empty view for creating a new document
    },
    handleSend() {
      // Perform a semantic search based on chatInput and selectedFiles
      // Reset chatInput after processing
      this.chatInput = '';
    },
  },
  mounted() {
    this.fetchFiles();
  },
};
</script>

<style scoped>
.pinedocs {
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: flex-end;
  padding: 1rem;
}

.file-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-gap: 1rem;
  padding: 1rem;
}

.file-card {
  display: flex;
  flex-direction: column;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 1rem;
  cursor: pointer;
}

.file-info {
  flex-grow: 1;
}

.file-options {
  display: flex;
  justify-content: flex-end;
}

.chat-input {
  padding: 1rem;
}
</style>
