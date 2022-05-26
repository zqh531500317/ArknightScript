import {get} from '@/api/http'

export const test = (fc) => {
    return get('test', fc)
}
export const testlist = () => {
    return get('testlist')
}