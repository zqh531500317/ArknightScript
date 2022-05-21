<template>
  <div>
    <el-card class="box-card" style="margin-bottom: 10px;min-height: 20px">
      <p>时间:{{ lizhi.time }}: 理智状态:{{ lizhi.lizhi }}/{{ lizhi.maxlizhi }}</p>
    </el-card>
    <el-card class="box-card" style="margin-bottom: 10px;min-height: 20px">
      <div slot="header">
        <span>运行中</span>
      </div>
      <p v-if="running_job_num===1">任务名称:{{ running_job.name }}</p>
    </el-card>
    <el-card class="box-card" style="margin-bottom: 10px;min-height: 20px">
      <div slot="header">
        <span>等待中---阻塞数量:{{ blocking_jobs_num }}</span>
      </div>
      <div v-for="(job,index) in blocking_jobs" :key="index">
        <p>任务名称:{{ job.name }}. 下次执行时间:{{ job.next_run_time }}</p>
      </div>
    </el-card>
    <el-card class="box-card" style="margin-bottom: 10px;">
      <div slot="header">
        <span>任务列表---数量:{{ this.$store.getters.jobs_num }}</span>
      </div>
      <div v-for="(job,index) in jobs" :key="index">
        <p>任务名称:{{ job.name }}. 下次执行时间:{{ job.next_run_time }}</p>
      </div>
    </el-card>
  </div>

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