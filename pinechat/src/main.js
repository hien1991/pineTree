import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

const isProduction = false; //Set true when deploying
const apiUrl = isProduction ? 'https://your-production-api-url.com' : 'http://localhost:5050';

const app = createApp(App);
app.config.globalProperties.$apiUrl = apiUrl;

app.use(store).use(router).mount('#app');
