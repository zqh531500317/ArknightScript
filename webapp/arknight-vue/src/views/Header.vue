<template>
  <el-header style="text-align: left; height:auto">
    <el-row>
      <el-col :xs="1" :sm="1" :md="1" :lg="1" :xl="2" style="padding-top: 8px">
        <el-tag color="#ffffff">当前模式：{{ mode }}</el-tag>
      </el-col>
      <el-col :xs="8" :sm="6" :md="4" :lg="3" :xl="1" style="padding-top: 8px">
        <spinner size="10"
                 :message="scheduleState"
                 :line-fg-color="scheduleStateMap[hashCode(scheduleState)].color"
                 :speed="scheduleStateMap[hashCode(scheduleState)].speed">
        </spinner>

      </el-col>
      <el-col :xs="15" :sm="6" :md="5" :lg="4" :xl="3" style="padding-top: 11px">
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
      <el-col :xs="8" :sm="8" :md="5" :lg="4" :xl="3" style="padding-top: 8px">
        <span class="tag-group__title">前端当前版本：</span>
        <el-tag color="#ffffff">{{ version }}</el-tag>

      </el-col>
      <el-col :xs="8" :sm="8" :md="5" :lg="4" :xl="3" style="padding-top: 8px">
        <span class="tag-group__title">前端最新版本：</span>
        <el-tag color="#ffffff">{{ latest_version }}</el-tag>
      </el-col>
      <el-col :xs="4" :sm="2" :md="1" :lg="1" :xl="1" style="padding-top: 10px"
              v-if="(mode === 'window' || mode === 'chrome') && updatable">
        <el-button @click="update" size="mini">{{ installdata }}</el-button>

      </el-col>
      <el-col :xs="8" :sm="6" :md="3" :lg="3" :xl="3" style="padding-top: 10px"
              v-if="(mode === 'window' || mode === 'chrome') && updatable">
        <el-alert
            :title="update_desc"
            type="info"
            show-icon>
        </el-alert>
      </el-col>
      <el-col v-if="false" :xs="8" :sm="8" :md="5" :lg="5" :xl="3" style="padding-top: 10px">
        屏幕宽度{{ windowWidth }}
        屏幕高度{{ windowHeight }}
      </el-col>
    </el-row>
  </el-header>
</template>
<script>

import {pause_scheduler_s, resume_scheduler_s} from '@/service/StateService'
import {mode, neu_version} from "@/config";
import Spinner from 'vue-simple-spinner'
import {mapMutations} from "vuex";
import {mapState} from "vuex";

export default {
  name: "HeaderView",
  data() {
    return {
      active_value: "运行中",
      inactive_value: "暂停中",
      mode: mode,
      scheduleStateMap: {},
      windowWidth: document.documentElement.clientWidth,  //实时屏幕宽度
      windowHeight: document.documentElement.clientHeight,   //实时屏幕高度
      installdata: "获取更新"
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
          console.log("try check update")
          let url = 'https://raw.githubusercontent.com/zqh531500317/arknight-script/master/webapp/update_manifest.json'
          let manifest = await window.Neutralino.updater.checkForUpdates(url);
          this.set_updatable([neu_version, manifest.version, neu_version !== manifest.version, manifest.data.desc])
        } catch (err) {
          console.log("check update error")
        }
      }

    },
    async update() {
      if (mode === "window" || mode === "chrome") {
        try {
          if (this.installdata === "获取更新") {
            console.log("try update")
            let res = await window.Neutralino.updater.install();
            console.log(res)
            console.log('安装完毕')
            if (res.success === true) {
              this.installdata = "立即重启更新"
            }
          } else if (this.installdata === "立即重启更新") {
            await window.Neutralino.app.restartProcess();
          }
        } catch (err) {
          console.log("update error")
        }
      }
    }
  },
  computed: {
    ...mapState(["version", 'latest_version', "updatable", 'update_desc']),
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
  mounted() {
    window.onresize = () => {
      return (() => {
        this.windowWidth = document.documentElement.clientWidth; //实时宽度
        this.windowHeight = document.documentElement.clientHeight; //实时高度
      })();
    };
  },
  created() {
    this.scheduleStateMap[this.hashCode('运行中')] = {"speed": 1, "color": "#2a6e3f"}
    this.scheduleStateMap[this.hashCode('暂停中')] = {"speed": 99999, "color": "#ffa502"}
    this.checkupdate()
    setInterval(this.checkupdate, 1000 * 60 * 10)

  }
}
</script>

<style scoped>

</style>