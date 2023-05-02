import { createRouter, createWebHashHistory } from "vue-router";
import ChatView from "./views/ChatView.vue";
import PineDocsView from "./views/PineDocsView.vue";

const routes = [
  { path: "/", component: ChatView },
  { path: "/pinedocs", component: PineDocsView },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
