<template>
  <div class="pinedocs">
    <div class="header">
      <upload-button @upload-success="fetchFiles"></upload-button>
      <button @click="handleNewDoc">New Doc</button>
    </div>
    <div class="file-grid">
      <div v-for="file in files" :key="file.id" @click="handleSelect(file.id)"
        :class="{ 'selected': selectedFiles.includes(file.id) }" class="file-card">
        <div class="file-info">
          <h3>{{ file.name }}</h3>
          <p>Uploaded: {{ file.uploadedDate }}</p>
          <p>Size: {{ file.size }}</p>
          <p>Chunks: {{ file.chunks }}</p>
        </div>
        <div class="file-options">
          <button @click.stop="handleDelete(file.id)">Delete</button>
          <div class="checkmark" v-if="selectedFiles.includes(file.id)">✓</div>
        </div>
      </div>
    </div>
    <ChatInput @send="handleSend" />
  </div>
  <error-modal :visible="errorModalVisible" :message="errorMessage" @dismiss="dismissError"></error-modal>
</template>

<script>
import ErrorModal from "@/components/common/ErrorModal.vue";
import UploadButton from "@/components/UploadButton.vue";
import ChatInput from './common/ChatInput.vue';
export default {
  name: "PineDocs",
  components: {
    ErrorModal,
    UploadButton,
    ChatInput,
  },
  data() {
    return {
      files: [], // Replace with actual files fetched from your database
      selectedFiles: [],
      chatInput: "",
      errorMessage: "",
      errorModalVisible: false,
    };
  },
  methods: {
    async fetchFiles() {
      try {
        const response = await fetch(`${this.$apiUrl}/get_all_uploads`);
        const uploadedFiles = await response.json();
        if (uploadedFiles.error) {
          this.errorMessage = uploadedFiles.error;
          this.errorModalVisible = true;
          console.error('Error fetching uploaded files:', uploadedFiles.error);
          return;
        }
        this.files = uploadedFiles.map((file) => ({
          id: file.id,
          name: file.filename,
          uploadedDate: file.timestamp,
          size: file.file_size,
          chunks: file.num_chunks,
        }));
      } catch (error) {
        this.errorMessage = 'Error fetching uploaded files';
        this.errorModalVisible = true;
        console.error('Error fetching uploaded files:', error);
      }
    },
    handleSelect(fileId) {
      console.log("You clicked fileId: ", fileId);
      const index = this.selectedFiles.indexOf(fileId);
      if (index === -1) {
        this.selectedFiles.push(fileId);
      } else {
        this.selectedFiles.splice(index, 1);
      }
      console.log("Selected files:", this.selectedFiles);
    },
    async handleDelete(fileId) {
      const confirmed = confirm("Are you sure you want to delete this file?");
      if (confirmed) {
        try {
          const file = this.files.find((file) => file.id === fileId);
          const response = await fetch(`${this.$apiUrl}/delete_file`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              filename: file.name,
            }),
          });
          const result = await response.json();
          if (result.status === "success") {
            this.fetchFiles();
          } else {
            this.errorMessage = result.message;
            this.errorModalVisible = true;
          }
        } catch (error) {
          this.errorMessage = "Error deleting file";
          this.errorModalVisible = true;
          console.error("Error deleting file:", error);
        }
      }
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
    handleSend(message, event) {
      if (event && event.shiftKey) {
        // If shift + enter is pressed, stop the event but don't send the message
        event.stopPropagation();
      } else {
        console.log("Message: ", message);
        // Call your API or other functions here, for example: this.fetchFiles();
      }
    },
    dismissError() {
      this.errorMessage = '';
      this.errorModalVisible = false;
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

.selected {
  background-color: #f0f0f0;
}

.file-info {
  flex-grow: 1;
}

.file-options {
  display: flex;
  justify-content: flex-end;
}

.checkmark {
  font-size: 18px;
  color: #3cba54;
  margin-left: 5px;
}
</style>