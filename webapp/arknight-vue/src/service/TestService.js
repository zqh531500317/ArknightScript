import {
    test
} from '@/api/test'
import {loading} from "@/util/utils";

export const test_service = async function (fc) {
    loading.open()
    await test(fc)
    loading.close()
}
