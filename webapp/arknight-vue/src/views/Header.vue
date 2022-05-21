<template>
  <el-header style="text-align: left; font-size: 12px;height:auto">
    <el-row>
      <el-col :span="2" style="height: auto">
        <el-tag color="#ffffff">当前模式：{{ mode }}</el-tag>
      </el-col>
      <el-col :span="2">
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
      <el-col :span="2" style="padding-top: 10px" v-if="mode === 'window' || mode === 'chrome'">
        <el-button @click="update">更新</el-button>
      </el-col>
    </el-row>


  </el-header>
</template>
<script>

import {pause_scheduler_s, resume_scheduler_s} from '@/service/StateService'
import {mode, neu_version} from "@/config";
import Spinner from 'vue-simple-spinner'
import {mapMutations} from "vuex";

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
    ...mapMutations(["set_updatable"]),
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

    },
    async checkupdate() {
      if (mode === 'window' || mode === 'chrome') {
        try {
          let url = 'https://raw.githubusercontent.com/zqh531500317/arknight-script/master/webapp/update_manifest.json'
          let manifest = await window.Neutralino.updater.checkForUpdates(url);
          console.log(manifest.version, "=====", neu_version)
          if (manifest.version !== neu_version) {
            //myMessage("有新的更新,当前版本:" + neu_version + " 最新版本:" + manifest.version)
            this.set_updatable(neu_version, manifest.version)
          }
        } catch (err) {
          console.log("check update error")
        }
      }

    },
    async update() {
      if (mode === "window" || mode === "chrome") {
        try {
          await window.Neutralino.updater.install();
          await window.Neutralino.app.restartProcess();
        } catch (err) {
          console.log("update error")
        }
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
    this.checkupdate()
  }
}
</script>

<style scoped>

</style>