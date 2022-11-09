import {recruit,scheduler} from "@/api/recruit";
import {loading} from "@/util/utils";

export const recruit_service = async function (recruitEntity) {
    loading.open()
    let response = await recruit(recruitEntity)
    console.log(new Date(), ":recruit:", response)
    loading.close()
}
export const scheduler_service = async function (schedulerEntity) {
    loading.open()
    let response = await scheduler(schedulerEntity)
    console.log(new Date(), ":scheduler:", response)
    loading.close()
}
export default () => {
}