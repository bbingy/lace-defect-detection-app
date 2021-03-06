import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import VueResource from 'vue-resource'
import VideoPlayer from 'vue-video-player'
import 'vue-video-player/src/custom-theme.css'
import 'video.js/dist/video-js.css'
  
Vue.use(VideoPlayer)

Vue.use(ElementUI)
Vue.use(VueResource);

new Vue({
  el: '#app',
  render: h => h(App)
})
