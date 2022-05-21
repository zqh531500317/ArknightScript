import Vue from 'vue'
import Vuex from 'vuex'
import action from '@/store/action'
import getters from '@/store/getters'
import mutations from '@/store/mutations'

Vue.use(Vuex)
const state = {
    version: "unsupport.1",
    latest_version: "unsupport.2",
    updatable: false,
    isLogin: false,
    fight_state: 'stop',
    scheduleState: "暂停中",
    lizhi: {
        time: "未获取",
        lizhi: "未获取",
        maxlizhi: "未获取"
    },
    jobs: [
        {name: "任务名称", next_run_time: Date()}
    ],
    fight_jobs: [],
    logList: [],
    running_job_num: 0,
    running_job: {
        id: "",
        name: ""
    },
    blocking_jobs: [],
    blocking_jobs_num: 0,

}

export default new Vuex.Store({
    state,
    getters,
    mutations,
    action
})