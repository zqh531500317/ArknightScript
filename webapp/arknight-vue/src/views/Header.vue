<template>
  <el-header style="text-align: left; font-size: 12px;height:auto">
    <el-row>
      <el-col :span="2" style="height: auto">
        <el-tag color="#ffffff">当前模式：{{ mode }}</el-tag>
      </el-col>
      <el-col :span="2" >
        <spinner size="10"
                 :message="scheduleState"
                 :line-fg-color="scheduleStateMap[hashCode(scheduleState)].color"
                 :speed="scheduleStateMap[hashCode(scheduleState)].speed">
        </spinner>

      </el-col>
      <el-col :span="4" style="padding-top: 10px">
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
    </el-col>
    </el-row>



  </el-header>
</template>
<script>

import {pause_scheduler_s, resume_scheduler_s} from '@/service/StateService'
import {mode} from "@/config";
import Spinner from 'vue-simple-spinner'

export default {
  name: "HeaderView",
  data() {
    return {
      active_value: "运行中",
      inactive_value: "暂停中",
      mode: mode,
      scheduleStateMap: {}
    }
  },
  methods: {
    hashCode(s) {
      return s.split("").reduce(function (a, b) {
        a = ((a << 5) - a) + b.charCodeAt(0);
        return a & a
      }, 0);
    },
    async changeScheduleState(state) {
      if (state === '暂停中') {
        pause_scheduler_s()
      } else {
        resume_scheduler_s()
      }

    }
  },
  computed: {
    scheduleState: {
      get() {
        return this.$store.state.scheduleState
      },
      set(value) {
        this.$store.commit('set_scheduler_state', value)
      }
    }
  },
  components: {
    Spinner
  },
  created() {
    this.scheduleStateMap[this.hashCode('运行中')] = {"speed": 1, "color": "#2a6e3f"}
    this.scheduleStateMap[this.hashCode('暂停中')] = {"speed": 99999, "color": "#ffa502"}

  }
}
</script>

<style scoped>

</style>