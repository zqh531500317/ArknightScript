import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueSocketIO from "vue-socket.io";
import SocketIO from "socket.io-client";
import store from '@/store/index'
import {base_url} from "@/util/utils";

Vue.config.productionTip = false
Vue.use(VueAxios, axios)
Vue.use(ElementUI);
Vue.use(new VueSocketIO(
    {
        connection: SocketIO(base_url + "/dcenter"),
        debug: false,
        extraHeaders: {"Access-Control-Allow-Origin": '*'},
    }
))
Vue.prototype.$addLive = function () {
    return this.$loading({
        lock: true,
        text: '提交中....',
        spinner: 'el-icon-loading',
        background: 'rgba(0,0,0,0.7)',
        target: document.querySelector('.submit-test-dialog')
    })
}
Vue.prototype.$success = function () {
    return this.$message({
        message: '操作成功',
        type: 'success'
    });
}
export let vue = new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
