<template>
    <div v-if="visible" class="error-modal">
        <div class="error-modal-content">
            <h3>Error</h3>
            <p>{{ message }}</p>
            <button @click="$emit('dismiss')">OK</button>
        </div>
    </div>
</template>
  
<script>
export default {
    props: {
        message: {
            type: String,
            default: "",
        },
        visible: {
            type: Boolean,
            default: false,
        },
    },
};
</script>
  
<style>
.error-modal {
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}

.error-modal-content {
    background-color: #f8f8f8;
    padding: 20px;
    border-radius: 5px;
    width: 80%;
    max-width: 400px;
    text-align: center;
}

.error-modal-content h3 {
    color: #f44336;
    margin: 0 0 10px;
}

.error-modal-content button {
    background-color: #f44336;
    color: white;
    border: none;
    padding: 10px 20px;
    margin-top: 15px;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
}

.error-modal-content button:hover {
    background-color: #d32f2f;
}
</style>
  