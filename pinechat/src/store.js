import { createStore } from 'vuex';

const initialState = {
  pineconeApiKey: localStorage.getItem('pineconeApiKey') || '',
  pineconeEnvKey: localStorage.getItem('pineconeEnvKey') || '',
  openaiApiKey: localStorage.getItem('openaiApiKey') || '',
};

export default createStore({
  state: initialState,
  mutations: {
    setPineconeApiKey(state, key) {
      state.pineconeApiKey = key;
    },
    setOpenaiApiKey(state, key) {
      state.openaiApiKey = key;
    },
    setPineconeEnvKey(state, key){
      state.pineconeEnvKey = key;
    }
  },
  actions: {
    updatePineconeApiKey({ commit }, key) {
      commit('setPineconeApiKey', key);
      localStorage.setItem('pineconeApiKey', key);
    },
    updateOpenaiApiKey({ commit }, key) {
      commit('setOpenaiApiKey', key);
      localStorage.setItem('openaiApiKey', key);
    },
    updatePineconeEnvKey({ commit }, key) {
      commit('setPineconeEnvKey', key);
      localStorage.setItem('pineconeEnvKey', key);
    },
  },
  getters: {
    getPineconeApiKey(state) {
      return state.pineconeApiKey;
    },
    getOpenaiApiKey(state) {
      return state.openaiApiKey;
    },
    getPineconeEnvKey(state) {
      return state.pineconeEnvKey;
    }
  },
});
