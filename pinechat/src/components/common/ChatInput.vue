<template>
    <div class="chat-input">
        <textarea v-model="message" @keydown.enter="sendMessage($event)" placeholder="Type your message"
            class="chat-textarea"></textarea>
        <button class="submit-button" @click="sendMessage($event)">
            <i class="material-icons">send</i>
        </button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            message: '',
        };
    },
    methods: {
        sendMessage(event) {
            if (event.shiftKey) {
                //Allows shift+enter to line-break w/o submitting
                event.stopPropagation();
            } else {
                this.$emit('send', this.message, event);
                this.message = '';
                event.preventDefault();
            }
        },
    },
};
</script>

<style scoped>
.chat-input {
    padding: 1rem;
    display: flex;
    align-items: end;
    justify-content: center;
}


.chat-textarea {
    width: 100%;
    max-width: 800px;
    height: 100%;
    padding: 10px;
    padding-right: 50px; 
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    outline: none;
    resize: vertical;
}

.chat-textarea:focus {
    border-color: #3cba54;
    box-shadow: 0 0 5px rgba(60, 186, 84, 0.2);
}

.submit-button {
    background-color: #3cba54;
    color: white;
    padding: 6px;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    outline: none;
    transition: background-color 0.2s;
    margin-left: -45px;
    margin-bottom: 5px;
}


.submit-button:hover {
    background-color: #2d9e45;
}

.material-icons {
    vertical-align: middle;
}
</style>
