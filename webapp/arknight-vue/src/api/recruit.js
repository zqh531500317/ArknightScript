import {get, post} from '@/api/http'

export const recruit = (recruitEntity) => {
    return post('/recruit', {'recruitEntity': recruitEntity})
}
export const scheduler = (schedulerEntity) => {
    return post('/scheduler', {'schedulerEntity': schedulerEntity})
}