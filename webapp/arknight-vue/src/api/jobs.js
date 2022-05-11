import {get, post} from '@/api/http'

export function get_jobs() {
    return get('/get_jobs')
}

export function get_job(ids) {
    return post('/get_job', {ids: ids})
}

export function get_fight_jobs() {
    return get('/get_fight_jobs')
}

export function del_fight_job(id) {
    return post('/del_fight_job', {id: id})
}

export function add_fight_job(temp) {
    return post('/add_fight_job', {
        fight: temp
    })
}

export function pause_or_resume(name, state) {
    return post('/pause_or_resume', {
        name: name,
        state: state
    })
}

export function trigger_change(value, kind, name) {
    return post('/trigger_change', {
        value: value,
        kind: kind,
        name: name
    })
}