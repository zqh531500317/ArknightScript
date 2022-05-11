<template>
  <el-header style="text-align: left; font-size: 12px;height:auto;min-height: 50px">
    <el-tag type="info">当前模式：{{ mode }}</el-tag>
    调度器:
    <el-switch
        v-model="scheduleState"
        active-color="#13ce66"
        inactive-color="#ff4949"
        active-text="运行中"
        inactive-text="暂停中"
        :active-value="active_value"
        :inactive-value="inactive_value"
        @change="changeScheduleState($event)">
    </el-switch>

  </el-header>
</template>
<script>

import {pause_scheduler_s, resume_scheduler_s} from '@/service/StateService'
import {mode} from "@/config";

export default {
  name: "HeaderView",
  data() {
    return {
      active_value: "运行中",
      inactive_value: "暂停中",
      mode: mode
    }
  },
  methods: {
    async changeScheduleState(state) {
      if (state === '暂停中') {
        pause_scheduler_s()
      } else {
        resume_scheduler_s()
      }

    }
  },
  computed: {
    scheduleState:{
      get(){
        return this.$store.state.scheduleState
      },
      set(value){
        this.$store.commit('set_scheduler_state',value)
      }
    }
  }
}
</script>

<style scoped>

</style>