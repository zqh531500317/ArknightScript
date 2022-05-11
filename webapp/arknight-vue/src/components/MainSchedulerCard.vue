<template>
  <el-card class="box-card" style="margin-bottom: 10px">
    <div slot="header">
      <span>{{ type }}</span>
    </div>
    <div v-for="(job) in jobList" :key="job.id">
      <el-row>
        <el-row class="pad">
          <el-switch
              v-model="job.state"
              active-color="#13ce66"
              inactive-color="#ff4949"
              :active-text="`开启${job.name}`"
              :inactive-text="`关闭${job.name}`"
              @change="state_change($event,job.id)">
          </el-switch>
        </el-row>
      </el-row>
      <el-row class="pad">
        <span class="input">cron表达式：</span>
        <el-input @change="trigger_change_m($event,'hour',job.id)"
                  v-model="job.hour"
                  class="input"
                  placeholder="时">
          <template slot="prepend">时</template>
        </el-input>
        <el-input @change="trigger_change_m($event,'minute',job.id)"
                  v-model="job.minute"
                  class="input"
                  placeholder="分">
          <template slot="prepend">分</template>
        </el-input>
      </el-row>
    </div>
  </el-card>
</template>

<script>
import {pause_or_resume_service, update_job_service} from "@/service/JobService";

export default {
  name: "MainSchudulerCard",
  props: ['type', 'jobList'],
  methods: {
    //暂停或恢复任务
    state_change(state, name) {
      pause_or_resume_service(name, state)
    },
    trigger_change_m(value, kind, name) {
      update_job_service(value, kind, name)
    }
  },
  created() {

  },
}
</script>

<style scoped>
.pad {
  padding: 5px;
  margin-bottom: 5px;
}
</style>