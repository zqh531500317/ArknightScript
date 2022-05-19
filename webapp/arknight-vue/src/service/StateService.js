import {
    get_lizhi,
    get_scheduler_state,
    isLogin,
    login,
    pause_scheduler,
    resume_scheduler,
    state_info
} from '@/api/state'
import {vue} from "@/main";
import {loading} from "@/util/utils";

export const get_lizhi_service = async function () {
    let response = await get_lizhi()
    console.log(new Date(), ":set_lizhi:", response)
    vue.$store.commit('set_lizhi', response)
}
export const get_scheduleState = async function () {
    let response = await get_scheduler_state()
    console.log(new Date(), ":get_scheduler_state:", response)
    vue.$store.commit('set_scheduler_state', response)
}
export const pause_scheduler_s = async function () {
    loading.open()
    let response = await pause_scheduler()
    console.log(new Date(), ":pause_scheduler:", response)
    vue.$store.commit('set_scheduler_state', response)
    loading.close()
}
export const resume_scheduler_s = async function () {
    loading.open()
    let response = await resume_scheduler()
    console.log(new Date(), ":resume_scheduler:", response)
    vue.$store.commit('set_scheduler_state', response)
    loading.close()

}
export const isLogin_service = async function () {
    let response = await isLogin()
    console.log(new Date(), ":isLogin:", response)
    vue.$store.commit('set_login_state', response)
}
export const login_submit_service = async function (user) {
    let response = await login(user)
    console.log(new Date(), ":login:", response)
    vue.$store.commit('set_login_state', response)
}
export const state_info_service = async function () {
    let response = await state_info()
    console.log(new Date(), ":state_info:", response)
    vue.$store.commit('set_state_info', response)
}
export default () => {
    get_lizhi_service()
    get_scheduleState()
    isLogin_service()
    state_info_service()
}