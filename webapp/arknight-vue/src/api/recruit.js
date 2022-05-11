import {get, post} from '@/api/http'

export const recruit = (recruitEntity) => {
    return post('/recruit', {'recruitEntity': recruitEntity})
}