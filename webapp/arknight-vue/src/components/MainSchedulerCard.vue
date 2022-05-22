<template>
  <div>
    <p>{{ type }}</p>
    <span class="line"></span>
    <el-row :gutter="10">
      <el-col :span="8" v-for="(job) in jobList" :key="job.id">
        <el-card class="box-card" style="margin-bottom: 10px">
          <div slot="header">
            <span>任务名称：{{ job.name }}</span>
          </div>
          <div>
            <el-switch
                class="space"
                v-model="job.state"
                active-color="#13ce66"
                inactive-color="#ff4949"
                :active-text="`开启`"
                :inactive-text="`关闭`"
                @change="state_change($event,job.id)">
            </el-switch>
          </div>
          <el-input @change="trigger_change_m($event,'hour',job.id)"
                    v-model="job.hour"
                    class="input space"
                    placeholder="时"
                    style="width: 180px">
            <template slot="prepend">h</template>
          </el-input>

          <el-input @change="trigger_change_m($event,'minute',job.id)"
                    v-model="job.minute"
                    class="input space"
                    placeholder="分"
                    style="width: 180px">
            <template slot="prepend">m</template>
          </el-input>
        </el-card>
      </el-col>
    </el-row>
  </div>

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