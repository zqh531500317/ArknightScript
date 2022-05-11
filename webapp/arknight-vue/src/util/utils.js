import {Loading, Message} from "element-ui";

function getUrl() {
    console.log(window.location.protocol)
    console.log(window.location.hostname)
    const pattern = /^(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9][0-9]|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9][0-9]|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9][0-9]|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9][0-9]|[0-9])$/;
    const isip = pattern.test(window.location.hostname);
    let port;
    if (isip || (window.location.hostname === "localhost")) {
        port = 5000
    } else {
        port = window.location.port
    }
    const base_url = window.location.protocol + "//" + window.location.hostname + ":" + port
    console.log(base_url)
    return base_url
}


export const base_url = getUrl()
export const handle_suggestion_map_name = function (queryString, cb) {
    function createFilter(queryString) {
        return (suggestion_map_name) => {
            return (suggestion_map_name.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
        };
    }

    let suggestion_map_names = [
        "1-7", "CA-5", "CE-6", "LS-6", "AP-5", "PR-A-1", "PR-A-2"
        , "PR-B-1", "PR-B-2", "PR-C-1", "PR-C-2", "PR-D-1", "PR-D-2"
    ]
    let temp = suggestion_map_names.map((e) => {
        return {
            value: e,
            name: ""
        }
    })
    let result = queryString ? temp.filter(createFilter(queryString)) : temp
    cb(result)
}

const loadOption = {
    fullscreen: true,
    lock: true,
    text: 'Loading',
    spinner: 'el-icon-loading',
    background: 'rgba(0, 0, 0, 0.7)'
}


class loadEvents {
    loadingInstance

    constructor(vueThis) {
        this.vm = vueThis;  //vue中的this  也可以不用
    }

    open() {
        this.loadingInstance = Loading.service(loadOption);
    }

    close(timeout = 200) {
        setTimeout(() => {
            this.loadingInstance.close();
        }, timeout);
    }
}

export const loading = new loadEvents()

export function message_success(msg = '操作成功') {
    Message.success(msg)
}

export function message_warning(msg = '操作异常') {
    Message.warning(msg)
}