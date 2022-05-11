import {vue} from "@/main";
import {fight,is_fight} from '@/api/fight'
import {message_success} from "@/util/utils";

export const fight_submit = async function (fight_instance) {
    message_success()
    let response = await fight(fight_instance)
    console.log(new Date(), ":fight_submit:", response)
    vue.$store.commit('set_fight_jobs', response)
}
export const is_fight_service = async function () {
    let response = await is_fight()
    console.log(new Date(), ":is_fight:", response)
    vue.$store.commit('set_fight_state', response)
}

export default () => {
    is_fight_service()
}