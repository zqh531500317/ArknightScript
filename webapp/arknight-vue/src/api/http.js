import axios from 'axios';//引入axios
import {base_url} from "@/util/utils";

//环境的切换 开发环境(development)使用的是测试接口  和   生产环境(production)使用的是上线接口
if (process.env.NODE_ENV === 'development') {
    //设置默认路径
    console.log('development')
    axios.defaults.baseURL = base_url
}
if (process.env.NODE_ENV === 'production') {
    console.log('production')
    axios.defaults.baseURL = base_url
} else {
    console.log(process.env.NODE_ENV)
    axios.defaults.baseURL = base_url
}
axios.defaults.timeout = 5000;//加载不出来5秒之后就是加载失败
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
//在main.js设置全局的请求次数，请求的间隙
axios.defaults.retry = 4;
axios.defaults.retryDelay = 10000;

axios.interceptors.response.use(undefined, function axiosRetryInterceptor(err) {
    let config = err.config;
    // If config does not exist or the retry option is not set, reject
    if (!config || !config.retry) return Promise.reject(err);

    // Set the variable for keeping track of the retry count
    config.__retryCount = config.__retryCount || 0;

    // Check if we've maxed out the total number of retries
    if (config.__retryCount >= config.retry) {
        // Reject with the error
        return Promise.reject(err);
    }

    // Increase the retry count
    config.__retryCount += 1;

    // Create new promise to handle exponential backoff
    let backoff = new Promise(function (resolve) {
        setTimeout(function () {
            resolve();
        }, config.retryDelay || 1);
    });

    // Return the promise in which recalls axios to retry the request
    return backoff.then(function () {
        return axios(config);
    });
});


// 使用promise返回axios请求的结果
export const get = (url, params) => {
    return new Promise((resolve, reject) => {
        axios.get(url, {
            params: params
        }).then(res => {
            resolve(res.data.result)
        }).catch(err => {
            reject(err)
        })
    })
}

export const post = (url, params) => {
    return new Promise((resolve, reject) => {
        axios.post(url, params).then(res => {
            resolve(res.data.result)
        }).catch(err => {
            reject(err.data)
        })

    })
}
//额外的axios实例
export const axiosInstance = axios.create({
    baseURL: base_url,
    timeout: 3000,
});