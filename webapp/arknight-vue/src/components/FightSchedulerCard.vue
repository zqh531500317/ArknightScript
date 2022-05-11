<template>

  <el-card class="box-card" style="margin-bottom: 10px">
    <div slot="header">
      <span>任务id：{{ job.id }}</span>
    </div>
    <el-row class="pad">
      <el-switch
          :value="job.state"
          active-color="#13ce66"
          inactive-color="#ff4949"
          active-text="开启任务"
          inactive-text="关闭任务"
          @change="state_change($event,job.id)">
      </el-switch>
    </el-row>
    <el-row class="pad">
      <el-input class="input" :value="job.map_name" disabled>
        <template slot="prepend">地图名称</template>
      </el-input>
    </el-row>
    <el-row class="pad">
      <el-input class="input" :value="job.times" disabled>
        <template slot="prepend">战斗次数</template>
      </el-input>
    </el-row>
    <el-row class="pad" :gutter="2">
      <el-col :span="8">
        <el-input class="input" :value="job.day_of_week" disabled style="width: auto">
          <template slot="prepend">w</template>
        </el-input>
      </el-col>
      <el-col :span="8">
        <el-input class="input" :value="job.hour" disabled style="width: auto">
          <template slot="prepend">h</template>
        </el-input>
      </el-col>
      <el-col :span="8">
        <el-input class="input" :value="job.minute" disabled style="width: auto">
          <template slot="prepend">m</template>
        </el-input>
      </el-col>
    </el-row>
    <el-row class="pad">
      <el-button type="danger" icon="el-icon-delete" @click="del_fight_job(job.id)">删除
      </el-button>
    </el-row>
  </el-card>


</template>

<script>
import {pause_or_resume_service, del_fight_job_service} from "@/service/JobService";

export default {
  name: "FightSchedulerCard",
  props: ['job'],
  methods: {
    //暂停或恢复任务

    state_change(state, name) {
      console.log(state, name)
      pause_or_resume_service(name, state)
    },
    del_fight_job(id) {
      del_fight_job_service(id)
    }
  }
}
</script>

<style scoped>

</style>