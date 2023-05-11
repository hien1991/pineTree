<template>
    <div class="chat-input">
        <div class="input-container">
            <textarea ref="textarea" v-model="message" @keydown.enter="handleKeyDown($event)" @input="resizeTextArea"
                placeholder="Type your message" class="chat-textarea"></textarea>
            <button class="submit-button" @click="sendMessage($event)">
                <img src="../../assets/send-icon.png" alt="Submit" />
            </button>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            message: '',
            MIN_HEIGHT: 36, //height in pixels
            MAX_HEIGHT: 100,
        };
    },
    methods: {
        sendMessage(event) {
            if (event && event.shiftKey) {
                event.stopPropagation();
            } else {
                this.$emit('send', this.message, event);
                this.message = '';
                event.preventDefault();
            }
        },
        handleKeyDown(event) {
            if (event.key === 'Enter') {
                if (event.shiftKey) {
                    event.stopPropagation();
                } else {
                    this.sendMessage(event);
                }
            }
        },
        resizeTextArea() {
            this.$nextTick(() => {
                let textarea = this.$refs.textarea;
                textarea.style.height = 'auto';
                const maxHeight = this.MAX_HEIGHT;
                const minHeight = this.MIN_HEIGHT;
                console.log("scrollHeight: " + textarea.scrollHeight);

                let newHeight = (textarea.scrollHeight <= 60) ? minHeight : Math.min(textarea.scrollHeight*0.8, maxHeight);
                textarea.style.height = `${newHeight}px`;
                textarea.style.overflowY = newHeight === maxHeight ? 'scroll' : 'hidden';
            });
        },
    },
};
</script>

<style scoped>
.input-container {
    position: relative;
    display: inline-flex;
    width: 100%;
    max-width: 800px;
}

.chat-input {
    padding: 1rem;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    position: relative;
}

.chat-textarea {
    width: 100%;
    height: 100%;
    padding: 10px;
    padding-right: 50px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    outline: none;
    resize: none;
}

.chat-textarea:focus {
    border-color: #3cba54;
    box-shadow: 0 0 5px rgba(60, 186, 84, 0.2);
}

.submit-button {
    position: absolute;
    bottom: 7.5px;
    right: -2.5px;
    background: transparent;
    border: none;
    cursor: pointer;
    outline: none;
    transition: opacity 0.2s;
    width: 45px;
    height: 25px;
}

.submit-button:hover {
    opacity: 0.7;
}

.submit-button img {
    width: 100%;
    height: 100%;
}
</style>