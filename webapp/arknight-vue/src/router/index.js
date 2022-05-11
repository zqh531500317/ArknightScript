import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store/index';
import {isLogin_service} from "@/service/StateService";
import {loading} from "@/util/utils";
Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        meta: {
            auth: true
        },
        component: () => import('@/views/main/DashBoard')
    },
    {
        path: '/login',
        component: () => import('@/views/main/Login')
    },
    {
        path: '/setting',
        meta: {
            auth: true
        },
        component: () => import('@/views/main/Setting')
    },
    {
        path: '/fight',
        meta: {
            auth: true
        },
        component: () => import('@/views/main/Fight')
    },
    {
        path: '/recruit',
        meta: {
            auth: true
        },
        component: () => import('@/views/main/Recruit')
    },
    {
        path: '/fightScheduler',
        meta: {
            auth: true
        },
        component: () => import('@/views/main/FightScheduler')
    },
    {
        path: '/mainScheduler',
        meta: {
            auth: true
        },
        component: () => import('@/views/main/MainScheduler')
    },
]

const router = new VueRouter({
    routes
})
// 登陆验证
router.beforeEach((to, from, next) => {
    isLogin_service().then(() => {
        console.log(to.meta.auth, store.state.isLogin)
        loading.open()
        if (to.meta.auth && !store.state.isLogin) {
            next(
                {
                    path: 'login'
                }
            )
        } else {
            next();
        }
        loading.close(0)
    })
});
export default router
