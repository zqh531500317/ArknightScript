import {get, post} from '@/api/http'

export const fight = (fight) => {
    return post('/fight', {'fight': fight})
}
export const is_fight = () => {
    return get('/is_fight')
}