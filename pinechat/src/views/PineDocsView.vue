<template>
    <div class="pine-docs-view">
        <PineDocs :dbResultsVisible="dbResultsVisible" />
    </div>
</template>
  
<script>
import PineDocs from "../components/PineDocs.vue";

export default {
    name: "PineDocsView",
    components: {
        PineDocs,
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
</style>
  