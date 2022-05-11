export default {
    set_logList(state, append_log) {
        if (state.logList.length > 500) {
            state.logList = state.logList.slice(-400)
        }
        state.logList.push(append_log)
    },
    set_jobs(state, jobs) {
        state.jobs = jobs
    },
    set_lizhi(state, lizhi) {
        state.lizhi = lizhi
    },
    set_fight_jobs(state, fight_jobs) {
        state.fight_jobs = fight_jobs
    },
    set_scheduler_state(state, scheduler_state) {
        state.scheduleState = scheduler_state
    },
    set_fight_state(state, fight_state) {
        state.fight_state = fight_state
    },
    set_login_state(state,login_flag){
        state.isLogin=login_flag
    }
}