/* eslint-disable */
import StateService from '@/service/StateService'
import FightService from "@/service/FightService";
import RecruitService from "@/service/RecruitService";
import JobService from "@/service/JobService";
import {interval_num, setMode} from "@/config";
import {get, axiosInstance} from '@/api/http'

export function update() {
    StateService()
    JobService()
    FightService()
    RecruitService()
}

function init_Neutralino() {
    if (typeof (NL_MODE) == 'undefined') {
        setMode('web')
        console.log('web')
    } else {
        window.Neutralino.init()
        setMode(NL_MODE)
        console.log(NL_MODE)
        console.log(NL_CWD)
        window.Neutralino.events.on('windowClose', () => {
                window.Neutralino.os.showMessageBox('Confirm',
                    'Are you sure you want to quit?',
                    'YES_NO', 'QUESTION').then((button) => {
                    if (button === 'YES') {
                        get('/shutdown').then((e) => {
                                console.log(e)
                                if (e === 'success') {
                                    window.Neutralino.app.exit();
                                }
                            }
                        ).catch(e => {
                            window.Neutralino.app.exit();
                        })
                    }
                });
            }
        );
        axiosInstance.get('/ping').then((response) => {
                console.log("back is running")
            }
        ).catch((err) => {
            console.log("back is not running,start back")
            window.Neutralino.os.execCommand('start_flask.py', {background: true})
        })

    }
}

import vuex from '@/store/index'

window.test = function () {
    console.log(JSON.stringify(vuex.state))
}
export default function init() {
    init_Neutralino()

    StateService()
    setInterval(StateService, interval_num)
    JobService()
    setInterval(JobService, interval_num)
    FightService()
    setInterval(FightService, interval_num)
    RecruitService()
    setInterval(RecruitService, interval_num)

}
