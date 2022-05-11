import {vue} from "@/main";
import {get_jobs, get_fight_jobs, pause_or_resume, del_fight_job, add_fight_job, trigger_change} from "@/api/jobs";
import {loading} from "@/util/utils";


export const get_jobs_service = async function () {
    let response = await get_jobs()
    console.log(new Date(), ":set_jobs:", response)
    vue.$store.commit('set_jobs', response)
}
export const get_fight_jobs_service = async function () {
    let response = await get_fight_jobs()
    console.log(new Date(), ":set_fight_jobs:", response)
    vue.$store.commit('set_fight_jobs', response)
}
export const del_fight_job_service = async function (id) {
    loading.open()
    let response = await del_fight_job(id)
    console.log(new Date(), ":del_fight_job:", response)
    get_jobs_service()
    get_fight_jobs_service()
    loading.close()


}
export const add_fight_job_service = async function (temp) {
    loading.open()
    let response = await add_fight_job(temp)
    console.log(new Date(), ":add_fight_job:", response)
    get_jobs_service()
    get_fight_jobs_service()
    loading.close()

}
export const pause_or_resume_service = async function (name, state) {
    loading.open()
    let response = await pause_or_resume(name, state)
    console.log(new Date(), ":pause_or_resume:", response)
    get_jobs_service()
    get_fight_jobs_service()
    loading.close()

}
export const update_job_service = async function (value, kind, name) {
    loading.open()
    let response = await trigger_change(value, kind, name)
    console.log(new Date(), ":trigger_change:", response)
    get_jobs_service()
    get_fight_jobs_service()
    loading.close()

}
export default () => {
    get_jobs_service()
    get_fight_jobs_service()

}