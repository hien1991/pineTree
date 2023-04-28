<template>
    <div class="typing-indicator">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
    </div>
</template>
  
<script>
export default {
    name: 'TypingLoader',
};
</script>
  
<style scoped>
.typing-indicator {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 5px;
    margin-top: 5px;
    margin-left: 1rem;
}

@keyframes typingIndicator {
    0% {
        opacity: 0;
    }

    50% {
        opacity: 1;
    }

    100% {
        opacity: 0;
    }
}

.dot {
    background-color: #8e9775;
    border-radius: 50%;
    width: 8px;
    height: 8px;
    margin: 0 2px;
    opacity: 0;
    animation: typingIndicator 1.2s infinite;
    animation-delay: 0s;
}

.dot:nth-child(2) {
    animation-delay: 0.4s;
}

.dot:nth-child(3) {
    animation-delay: 0.8s;
}
</style>
  