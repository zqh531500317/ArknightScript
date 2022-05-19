import {get,post} from '@/api/http'

export const get_lizhi = () => {
    return get('/lizhi')
}
export const pause_scheduler = () => {
    return get('/pause_scheduler')
}
export const resume_scheduler = () => {
    return get('/resume_scheduler')
}
export const get_scheduler_state = () => {
    return get('/is_scheduler_running')
}
export const ping = () => {
    return get('ping')
}
export const isLogin = () => {
    return get('isLogin')
}
export const login = (form) => {
    return post('login',{form:form})
}
export const state_info = () => {
    return get('state_info',)
}