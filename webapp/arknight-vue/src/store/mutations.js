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
    set_login_state(state, login_flag) {
        state.isLogin = login_flag
    },
    set_state_info(state, state_info) {
        state.running_job_num = state_info.running_job_num
        state.running_job.id = state_info.running_job.id
        state.running_job.name = state_info.running_job.name
        state.blocking_jobs = state_info.blocking_jobs
        state.blocking_jobs_num = state_info.blocking_jobs.length
    },
    set_updatable(state, t) {
        const version = t[0]
        const latest_version = t[1]
        state.version = version
        state.latest_version = latest_version
        state.updatable = t[2]
        console.log(version, "=====", latest_version, "=======", state.updatable)
    }
}