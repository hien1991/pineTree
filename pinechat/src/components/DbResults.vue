<template>
    <div class="database-results">
        <div class="search-query-display" v-if="searchQueryDisplay">
            <strong>Database Query:</strong> "{{ searchQueryDisplay }}"
        </div>
        <div class="search-controls">
            <input type="text" v-model="searchQuery" @input="filterResults" placeholder="Search..." />
        </div>
        <div class="results-list">
            <!-- Iterate through search results and display them in collapsible cards -->
            <div v-for="(result, index) in filteredResults" :key="index" class="result-card">
                <div class="result-header" @click="toggleCollapse(index)">
                    <h2>{{ result.title }}</h2>
                    <span class="timestamp">{{ result.timestamp }}</span>
                    <span class="source">{{ result.source }}</span>
                </div>
                <div v-show="!result.collapsed" class="result-content">
                    <p>{{ result.text }}</p>
                </div>
            </div>
        </div>
        <div class="pagination">
            <!-- Add pagination controls here -->
        </div>
    </div>
</template>
  
<script>
export default {
    name: "DbResults",
    props: {
        results: {
            type: Array,
            default: () => [],
        },
        searchQueryDisplay: {
            type: String,
            default: '',
        },
    },
    data() {
        return {
            searchQuery: "",
            filteredResults: [],
        };
    },
    watch: {
        results: {
            immediate: true,
            handler() {
                this.filteredResults = this.results.map((result) => ({ ...result, collapsed: false }));
            },
        },
    },
    methods: {
        toggleCollapse(index) {
            this.filteredResults[index].collapsed = !this.filteredResults[index].collapsed;
        },
        filterResults() {
            const query = this.searchQuery.toLowerCase();
            this.filteredResults = this.results.filter(
                (result) => result.title.toLowerCase().includes(query) || (result.text && result.text.toLowerCase().includes(query)),
            );
        },

    },
};
</script>
  
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&display=swap");

.database-results {
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 800px;
    margin: 20px auto;
    padding: 10px;
    border: 1px solid #e6e6e6;
    border-radius: 4px;
    background-color: #f4f1ea;
    font-family: "Roboto", sans-serif;
}

.search-controls {
    display: flex;
    width: 100%;
    margin-bottom: 20px;
}

.search-controls input {
    flex-grow: 1;
    padding: 10px;
    border: 1px solid #dcd9d5;
    border-radius: 4px;
    font-size: 16px;
    outline: none;
    transition: border-color 0.3s;
}

.search-controls input:focus {
    border-color: #a0aec0;
}

.search-query-display {
    font-size: 0.9em;
    margin-bottom: 10px;
    color: #666;
    text-align: center;
    width: 100%;
    background-color: #e6e6e6;
    padding: 5px;
    border-radius: 4px;
}

.result-card {
    display: flex;
    flex-direction: column;
    width: 100%;
    margin-bottom: 20px;
    border: 1px solid #dcd9d5;
    border-radius: 4px;
    background-color: #ffffff;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s;
}

.result-card:hover {
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

.result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    font-size: 1.1em;
    font-weight: 600;
    border-bottom: 1px solid #dcd9d5;
    cursor: pointer;
    background-image: none;
    background-size: 8px 8px;
}

.result-content {
    padding: 10px;
}

.timestamp,
.source {
    font-size: 0.8em;
    font-weight: 400;
    color: #999999;
}

.timestamp {
    margin-left: 10px;
}

.source {
    margin-right: 10px;
}

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    margin-top: 20px;
}
</style>
