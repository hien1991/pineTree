<template>
    <div class="chat-view">
        <ChatWindow :dbResultsVisible="dbResultsVisible" />
    </div>
</template>
  
<script>
import ChatWindow from "../components/ChatWindow.vue";

export default {
    name: "ChatView",
    components: {
        ChatWindow,
    },
    props: {
        dbResultsVisible: {
            type: Boolean,
            default: false,
        },
    },
};
</script>
  
<style scoped>
.chat-view {
    /* Add custom styles for the ChatView here */
}
</style>
  