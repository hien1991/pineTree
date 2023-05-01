(function(){"use strict";var e={9527:function(e,t,s){var n=s(9242),i=s(3396);const o={id:"app"},a={class:"top-nav"},l={key:0,class:"guide-modal"},r={class:"guide-modal-content"},c=(0,i._)("h2",null,"Welcome to PineChat!",-1),p=(0,i._)("p",null,"Before you can start using the app, please enter the required API keys in the settings.",-1);function u(e,t,s,n,u,d){const h=(0,i.up)("SideChatBar"),y=(0,i.up)("ChatWindow"),g=(0,i.up)("SettingsModal");return(0,i.wg)(),(0,i.iD)(i.HY,null,[(0,i._)("div",o,[(0,i._)("nav",a,[(0,i._)("button",{onClick:t[0]||(t[0]=(...e)=>d.toggleDbResults&&d.toggleDbResults(...e))},"Show Datababase Returns"),(0,i._)("button",{onClick:t[1]||(t[1]=(...e)=>d.showSettings&&d.showSettings(...e))},"Settings")]),(0,i.Wm)(h),(0,i.Wm)(y,{dbResultsVisible:u.dbResultsVisible},null,8,["dbResultsVisible"]),u.settingsVisible?((0,i.wg)(),(0,i.j4)(g,{key:0,onClose:d.showSettings,onApiKeysUpdated:d.initializeBackend},null,8,["onClose","onApiKeysUpdated"])):(0,i.kq)("",!0)]),u.showGuideModal?((0,i.wg)(),(0,i.iD)("div",l,[(0,i._)("div",r,[c,p,(0,i._)("button",{onClick:t[2]||(t[2]=(...e)=>d.hideGuideModalAndShowSettings&&d.hideGuideModalAndShowSettings(...e))},"Go to Settings")])])):(0,i.kq)("",!0)],64)}var d=s(7139);const h=e=>((0,i.dD)("data-v-40a98e3e"),e=e(),(0,i.Cn)(),e),y={class:"settings-modal"},g={class:"settings-modal-content"},v=h((()=>(0,i._)("h2",null,"Settings",-1))),m=h((()=>(0,i._)("label",{for:"openai-api-key"},"OpenAI API Key:",-1))),f=h((()=>(0,i._)("label",{for:"pinecone-api-key"},"Pinecone API Key:",-1))),K=h((()=>(0,i._)("label",{for:"pinecone-api-key"},"Pinecone env:",-1))),b=h((()=>(0,i._)("label",{for:"model-selection"},"Use GPT-4 Model:",-1))),w={class:"success-message"};function _(e,t,s,o,a,l){return(0,i.wg)(),(0,i.iD)("div",y,[(0,i._)("div",g,[v,m,(0,i.wy)((0,i._)("input",{type:"text",id:"openai-api-key","onUpdate:modelValue":t[0]||(t[0]=e=>l.openaiApiKey=e)},null,512),[[n.nr,l.openaiApiKey]]),f,(0,i.wy)((0,i._)("input",{type:"text",id:"pinecone-api-key","onUpdate:modelValue":t[1]||(t[1]=e=>l.pineconeApiKey=e)},null,512),[[n.nr,l.pineconeApiKey]]),K,(0,i.wy)((0,i._)("input",{type:"text",id:"pinecone-env-key","onUpdate:modelValue":t[2]||(t[2]=e=>l.pineconeEnvKey=e)},null,512),[[n.nr,l.pineconeEnvKey]]),b,(0,i.wy)((0,i._)("input",{type:"checkbox",id:"model-selection","onUpdate:modelValue":t[3]||(t[3]=e=>l.useGpt4Model=e)},null,512),[[n.e8,l.useGpt4Model]]),(0,i._)("button",{onClick:t[4]||(t[4]=(...e)=>l.saveKeys&&l.saveKeys(...e))},"Save"),(0,i._)("button",{onClick:t[5]||(t[5]=t=>e.$emit("close"))},"Close"),(0,i._)("p",w,(0,d.zw)(a.successMessage),1)])])}var A=s(65),k={name:"SettingsModal",data(){return{successMessage:""}},computed:{...(0,A.Se)(["getPineconeApiKey","getPineconeEnvKey","getOpenaiApiKey","getUseGpt4Model"]),pineconeApiKey:{get(){return this.getPineconeApiKey},set(e){this.updatePineconeApiKey(e)}},pineconeEnvKey:{get(){return this.getPineconeEnvKey},set(e){this.updatePineconeEnvKey(e)}},openaiApiKey:{get(){return this.getOpenaiApiKey},set(e){this.updateOpenaiApiKey(e)}},useGpt4Model:{get(){return this.getUseGpt4Model},set(e){this.updateUseGpt4Model(e)}}},emits:["close"],methods:{...(0,A.nv)(["updatePineconeApiKey","updatePineconeEnvKey","updateOpenaiApiKey","updateUseGpt4Model"]),saveKeys(){this.$emit("api-keys-updated"),this.showSuccessMessage(),setTimeout((()=>{this.$emit("close")}),1500)},showSuccessMessage(){this.successMessage="API keys saved successfully!",setTimeout((()=>{this.successMessage=""}),1500)}}},S=s(89);const M=(0,S.Z)(k,[["render",_],["__scopeId","data-v-40a98e3e"]]);var D=M;const C=e=>((0,i.dD)("data-v-54533d7b"),e=e(),(0,i.Cn)(),e),I={class:"chat-container"},x=C((()=>(0,i._)("div",{class:"chat-header"},[(0,i._)("h1",null,"PineChat")],-1))),R={class:"chat-window"},T={class:"chat-messages",ref:"chatMessages"},P=C((()=>(0,i._)("div",{class:"spacer"},null,-1))),G={class:"message-bubble"},U={class:"chat-input"};function E(e,t,s,o,a,l){const r=(0,i.up)("TypingLoader"),c=(0,i.up)("UploadButton"),p=(0,i.up)("DbResults");return(0,i.wg)(),(0,i.iD)("div",I,[x,(0,i._)("div",R,[(0,i._)("div",T,[P,((0,i.wg)(!0),(0,i.iD)(i.HY,null,(0,i.Ko)(a.messages.slice().reverse(),((e,t)=>((0,i.wg)(),(0,i.iD)("div",{key:t,class:(0,d.C_)([e.type,"message"])},[(0,i._)("div",G,(0,d.zw)(e.text),1),a.isTyping&&0===t?((0,i.wg)(),(0,i.j4)(r,{key:0})):(0,i.kq)("",!0)],2)))),128))],512),(0,i._)("button",{class:"scroll-down",onClick:t[0]||(t[0]=(...e)=>l.scrollToBottom&&l.scrollToBottom(...e))},"↓")]),(0,i._)("div",U,[(0,i.wy)((0,i._)("textarea",{"onUpdate:modelValue":t[1]||(t[1]=e=>a.inputText=e),onKeydown:[t[2]||(t[2]=(0,n.D2)((0,n.iM)(((...e)=>l.submitMessage&&l.submitMessage(...e)),["exact","prevent"]),["enter"])),t[3]||(t[3]=(0,n.D2)((0,n.iM)(((...e)=>l.handleKeyDown&&l.handleKeyDown(...e)),["shift","exact"]),["enter"]))],onInput:t[4]||(t[4]=(...e)=>l.resizeInput&&l.resizeInput(...e)),style:{resize:"none",overflow:"hidden"},class:"chat-input-field",placeholder:"Send a message."},null,544),[[n.nr,a.inputText]]),(0,i._)("button",{onClick:t[5]||(t[5]=(...e)=>l.submitMessage&&l.submitMessage(...e))},"Send"),(0,i.Wm)(c)]),(0,i._)("div",{class:"db-results-wrapper",style:(0,d.j5)({display:s.dbResultsVisible?"block":"none"})},[s.dbResultsVisible?((0,i.wg)(),(0,i.j4)(p,{key:0,results:a.searchResults,searchQueryDisplay:a.searchQueryDisplay},null,8,["results","searchQueryDisplay"])):(0,i.kq)("",!0)],4)])}s(7658);var O=s(4161);const V=e=>((0,i.dD)("data-v-4acc7736"),e=e(),(0,i.Cn)(),e),z={class:"database-results"},$={key:0,class:"search-query-display"},B=V((()=>(0,i._)("strong",null,"Database Query:",-1))),Q={class:"search-controls"},j={class:"results-list"},Z=["onClick"],F={class:"timestamp"},q={class:"source"},W={class:"result-content"},H=V((()=>(0,i._)("div",{class:"pagination"},null,-1)));function L(e,t,s,o,a,l){return(0,i.wg)(),(0,i.iD)("div",z,[s.searchQueryDisplay?((0,i.wg)(),(0,i.iD)("div",$,[B,(0,i.Uk)(' "'+(0,d.zw)(s.searchQueryDisplay)+'" ',1)])):(0,i.kq)("",!0),(0,i._)("div",Q,[(0,i.wy)((0,i._)("input",{type:"text","onUpdate:modelValue":t[0]||(t[0]=e=>a.searchQuery=e),onInput:t[1]||(t[1]=(...e)=>l.filterResults&&l.filterResults(...e)),placeholder:"Search..."},null,544),[[n.nr,a.searchQuery]])]),(0,i._)("div",j,[((0,i.wg)(!0),(0,i.iD)(i.HY,null,(0,i.Ko)(a.filteredResults,((e,t)=>((0,i.wg)(),(0,i.iD)("div",{key:t,class:"result-card"},[(0,i._)("div",{class:"result-header",onClick:e=>l.toggleCollapse(t)},[(0,i._)("h2",null,(0,d.zw)(e.title),1),(0,i._)("span",F,(0,d.zw)(e.timestamp),1),(0,i._)("span",q,(0,d.zw)(e.source),1)],8,Z),(0,i.wy)((0,i._)("div",W,[(0,i._)("p",null,(0,d.zw)(e.text),1)],512),[[n.F8,!e.collapsed]])])))),128))]),H])}var Y={name:"DbResults",props:{results:{type:Array,default:()=>[]},searchQueryDisplay:{type:String,default:""}},data(){return{searchQuery:"",filteredResults:[]}},watch:{results:{immediate:!0,handler(){this.filteredResults=this.results.map((e=>({...e,collapsed:!1})))}}},methods:{toggleCollapse(e){this.filteredResults[e].collapsed=!this.filteredResults[e].collapsed},filterResults(){const e=this.searchQuery.toLowerCase();this.filteredResults=this.results.filter((t=>t.title.toLowerCase().includes(e)||t.text&&t.text.toLowerCase().includes(e)))}}};const J=(0,S.Z)(Y,[["render",L],["__scopeId","data-v-4acc7736"]]);var N=J,X=s.p+"img/upload-icon.5db7b317.png";const ee=e=>((0,i.dD)("data-v-4661d07f"),e=e(),(0,i.Cn)(),e),te={class:"upload-wrapper"},se=ee((()=>(0,i._)("img",{src:X,alt:"Uploads Icon"},null,-1))),ne=[se];function ie(e,t,s,n,o,a){return(0,i.wg)(),(0,i.iD)("div",te,[(0,i._)("input",{type:"file",ref:"fileInput",onChange:t[0]||(t[0]=(...e)=>a.uploadFile&&a.uploadFile(...e)),style:{display:"none"}},null,544),(0,i._)("button",{class:"upload-button",onClick:t[1]||(t[1]=(...e)=>a.openFileChooser&&a.openFileChooser(...e))},ne)])}var oe={name:"UploadButton",methods:{openFileChooser(){this.$refs.fileInput.click()},async uploadFile(){const e=new FormData;e.append("file",this.$refs.fileInput.files[0]);try{const t=await O.Z.post(`${this.$apiUrl}/upload`,e,{headers:{"Content-Type":"multipart/form-data"}});console.log(t.data)}catch(t){console.error("Error uploading file:",t)}}}};const ae=(0,S.Z)(oe,[["render",ie],["__scopeId","data-v-4661d07f"]]);var le=ae;const re=e=>((0,i.dD)("data-v-2e3824f7"),e=e(),(0,i.Cn)(),e),ce={class:"typing-indicator"},pe=re((()=>(0,i._)("span",{class:"dot"},null,-1))),ue=re((()=>(0,i._)("span",{class:"dot"},null,-1))),de=re((()=>(0,i._)("span",{class:"dot"},null,-1))),he=[pe,ue,de];function ye(e,t,s,n,o,a){return(0,i.wg)(),(0,i.iD)("div",ce,he)}var ge={name:"TypingLoader"};const ve=(0,S.Z)(ge,[["render",ye],["__scopeId","data-v-2e3824f7"]]);var me=ve,fe={name:"ChatWindow",components:{DbResults:N,UploadButton:le,TypingLoader:me},data(){return{inputText:"",messages:[],isTyping:!1,searchResults:[],searchQueryDisplay:""}},props:{dbResultsVisible:{type:Boolean,default:!1}},methods:{scrollToBottom(){this.$nextTick((()=>{let e=this.$refs.chatMessages.scrollHeight;window.scrollTo(0,e)}))},async submitMessage(){if(this.inputText.trim()){this.messages.push({type:"user",text:this.inputText}),this.isTyping=!0;try{O.Z.post(`${this.$apiUrl}/chat`,{input_text:this.inputText}).then((e=>{console.log(e.data);const t=e.data.response;this.searchResults=e.data.search_results,this.searchQueryDisplay=e.data.db_query;const s=t;this.messages.push({type:"bot",text:s}),this.isTyping=!1}))}catch(e){console.error("Error while communicating with chatbot:",e),this.messages.push({type:"error",text:"Error while communicating with chatbot"}),this.isTyping=!1}this.inputText=""}},handleKeyDown(e){if("Enter"===e.key&&e.shiftKey){e.preventDefault();const t=e.target,s=t.selectionStart;t.setRangeText("\n",s,s,"end"),t.setSelectionRange(s+1,s+1),this.inputText=t.value,this.resizeInput(e)}},resizeInput(e){const t=e.target;t.style.height="auto";const s=100,n=35;let i=t.scrollHeight<=51?n:Math.min(t.scrollHeight,s);t.style.height=`${i}px`,t.style.overflowY=i===s?"scroll":"hidden"}}};const Ke=(0,S.Z)(fe,[["render",E],["__scopeId","data-v-54533d7b"]]);var be=Ke;const we={class:"sidechatbar"};function _e(e,t,s,n,o,a){return(0,i.wg)(),(0,i.iD)("div",we)}var Ae={name:"SideChatBar",data(){return{}},methods:{}};const ke=(0,S.Z)(Ae,[["render",_e],["__scopeId","data-v-3c46d146"]]);var Se=ke,Me={name:"App",components:{ChatWindow:be,SideChatBar:Se,SettingsModal:D},data(){return{settingsVisible:!1,showGuideModal:!1,dbResultsVisible:!1}},methods:{showSettings(){this.settingsVisible=!this.settingsVisible},toggleDbResults(){this.dbResultsVisible=!this.dbResultsVisible},hideGuideModalAndShowSettings(){this.showGuideModal=!1,this.showSettings()},initializeBackend(){console.log("initializing backend...");const e=localStorage.getItem("openaiApiKey"),t=localStorage.getItem("pineconeApiKey"),s=localStorage.getItem("pineconeEnvKey"),n=localStorage.getItem("useGpt4Key");e&&t&&s&&O.Z.post(`${this.$apiUrl}/initialize`,{openaiApiKey:e,pineconeApiKey:t,pineconeEnvKey:s,useGpt4ModelKey:n})}},mounted(){this.initializeBackend();const e=localStorage.getItem("openaiApiKey"),t=localStorage.getItem("pineconeApiKey"),s=localStorage.getItem("pineconeEnvKey");e&&t&&s||(this.showGuideModal=!0)}};const De=(0,S.Z)(Me,[["render",u]]);var Ce=De;const Ie={pineconeApiKey:localStorage.getItem("pineconeApiKey")||"",pineconeEnvKey:localStorage.getItem("pineconeEnvKey")||"",openaiApiKey:localStorage.getItem("openaiApiKey")||"",useGpt4ModelKey:localStorage.getItem("openaiApiKey")||!1};var xe=(0,A.MT)({state:Ie,mutations:{setPineconeApiKey(e,t){e.pineconeApiKey=t},setOpenaiApiKey(e,t){e.openaiApiKey=t},setPineconeEnvKey(e,t){e.pineconeEnvKey=t},setUseGpt4ModelKey(e,t){e.useGpt4ModelKey=t}},actions:{updatePineconeApiKey({commit:e},t){e("setPineconeApiKey",t),localStorage.setItem("pineconeApiKey",t)},updateOpenaiApiKey({commit:e},t){e("setOpenaiApiKey",t),localStorage.setItem("openaiApiKey",t)},updatePineconeEnvKey({commit:e},t){e("setPineconeEnvKey",t),localStorage.setItem("pineconeEnvKey",t)},updateUseGpt4ModekKey({commit:e},t){e("setUseGpt4ModelKey",t),localStorage.setItem("useGpt4ModelKey",t)}},getters:{getPineconeApiKey(e){return e.pineconeApiKey},getOpenaiApiKey(e){return e.openaiApiKey},getPineconeEnvKey(e){return e.pineconeEnvKey},getUseGpt4ModelKey(e){return e.useGpt4ModelKey}}});const Re=!1,Te=Re?"https://your-production-api-url.com":"http://localhost:5050",Pe=(0,n.ri)(Ce);Pe.config.globalProperties.$apiUrl=Te,Pe.use(xe).mount("#app")}},t={};function s(n){var i=t[n];if(void 0!==i)return i.exports;var o=t[n]={exports:{}};return e[n](o,o.exports,s),o.exports}s.m=e,function(){var e=[];s.O=function(t,n,i,o){if(!n){var a=1/0;for(p=0;p<e.length;p++){n=e[p][0],i=e[p][1],o=e[p][2];for(var l=!0,r=0;r<n.length;r++)(!1&o||a>=o)&&Object.keys(s.O).every((function(e){return s.O[e](n[r])}))?n.splice(r--,1):(l=!1,o<a&&(a=o));if(l){e.splice(p--,1);var c=i();void 0!==c&&(t=c)}}return t}o=o||0;for(var p=e.length;p>0&&e[p-1][2]>o;p--)e[p]=e[p-1];e[p]=[n,i,o]}}(),function(){s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,{a:t}),t}}(),function(){s.d=function(e,t){for(var n in t)s.o(t,n)&&!s.o(e,n)&&Object.defineProperty(e,n,{enumerable:!0,get:t[n]})}}(),function(){s.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){s.p=""}(),function(){var e={143:0};s.O.j=function(t){return 0===e[t]};var t=function(t,n){var i,o,a=n[0],l=n[1],r=n[2],c=0;if(a.some((function(t){return 0!==e[t]}))){for(i in l)s.o(l,i)&&(s.m[i]=l[i]);if(r)var p=r(s)}for(t&&t(n);c<a.length;c++)o=a[c],s.o(e,o)&&e[o]&&e[o][0](),e[o]=0;return s.O(p)},n=self["webpackChunkpinechat"]=self["webpackChunkpinechat"]||[];n.forEach(t.bind(null,0)),n.push=t.bind(null,n.push.bind(n))}();var n=s.O(void 0,[998],(function(){return s(9527)}));n=s.O(n)})();
//# sourceMappingURL=app.8a86d985.js.map