<template>
  <el-card class="box-card" style="margin-bottom: 10px;">
    <p>{{ running_job_num }}</p>
    <p>{{ running_job }}</p>
    <p>{{ blocking_jobs }}</p>
    <p>{{ blocking_jobs_num }}</p>
    <p>时间:{{ lizhi.time }}: 理智状态:{{ lizhi.lizhi }}/{{ lizhi.maxlizhi }}</p>
    <div class="line"></div>
    <p>任务总数:{{ this.$store.getters.jobs_num }}</p>
    <div class="line"></div>
    <div v-for="job in jobs" :key="job.name">
      <p>任务名称:{{ job.name }}. 下次执行时间:{{ job.next_run_time }}</p>
    </div>
  </el-card>
</template>

<script>
import {get_jobs} from '@/api/jobs'
import {get_lizhi} from '@/api/state'
import {mapMutations, mapState} from 'vuex'

export default {
  name: "JobList",
  data() {
    return {}
  },
  computed: {
    ...mapState(['jobs', 'lizhi', 'running_job_num', 'running_job', 'blocking_jobs', 'blocking_jobs_num']),
  },
  methods: {
    ...mapMutations(['set_jobs', 'set_lizhi']),

  },
  async mounted() {
    let jobs = await get_jobs()
    console.log(jobs)
    this.set_jobs(jobs)
    let state = await get_lizhi()
    console.log(jobs)
    this.set_lizhi(state)
  }
}
</script>

<style scoped>

</style>