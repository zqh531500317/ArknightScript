<template>
  <div>
    <main-scheduler-card type="收获" :jobList="receive_job"></main-scheduler-card>
    <main-scheduler-card type="基建" :jobList="jijian_job"></main-scheduler-card>
    <main-scheduler-card type="信息" :jobList="message_job"></main-scheduler-card>
  </div>
</template>

<script>
import {get_job} from '@/api/jobs'
import mainSchedulerCard from '@/components/MainSchedulerCard'

export default {
  name: "MainSchudelerView",
  data() {
    return {
      receive_ids: {
        "receive_renwu": {},
        "friend": {},
        "receive_xinyong": {},
        "buy_xinyong_shop": {},
        "recruit_daily": {},

      }, jijian_ids: {
        "jijian_receive": {},
        "use_electricity": {},
        "clue": {},

      }, message_ids: {
        "get_lizhi": {},
        "xinpian": {},

      },
      receive_job: [], jijian_job: [], message_job: [],

    }
  },
  methods: {
    async get_receive_job() {
      let response = await get_job(this.receive_ids)
      console.log(response)
      this.receive_job = response
    },
    async get_jijian_job() {
      let response = await get_job(this.jijian_ids)
      console.log(response)
      this.jijian_job = response
    },
    async get_message_job() {
      let response = await get_job(this.message_ids)
      console.log(response)
      this.message_job = response
    }
  },
  created() {
    this.get_receive_job()
    this.get_jijian_job()
    this.get_message_job()
  },
  components: {
    mainSchedulerCard
  }
}
</script>

<style scoped>

</style>