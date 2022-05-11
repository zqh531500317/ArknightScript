import {recruit} from "@/api/recruit";
import {loading} from "@/util/utils";

export const recruit_service = async function (recruitEntity) {
    loading.open()
    let response = await recruit(recruitEntity)
    console.log(new Date(), ":recruit:", response)
    loading.close()
}
export default () => {
}