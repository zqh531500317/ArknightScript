<template>
  <el-card class="box-card" style="margin-bottom: 10px">
    <div slot="header">
      <span>添加任务</span>
    </div>
    <el-form ref="temp" :model="temp" label-width="100px">
      <el-form-item label="任务唯一id(以fight_开头)">
        <el-input v-model="temp.id">
        </el-input>
      </el-form-item>
      <el-form-item label="地图名称">
        <el-autocomplete
            class="inline-input"
            v-model="temp.map_name"
            :fetch-suggestions="handle_suggestion_map_name"
            placeholder="请输入内容"
        ></el-autocomplete>
      </el-form-item>
      <el-form-item label="地图类型">
        <el-radio-group v-model="temp.type">
          <el-radio label="主线" value="1"></el-radio>
          <el-radio label="资源收集" value="2"></el-radio>
          <el-radio label="剿灭" value="3"></el-radio>
          <el-radio label="活动" value="4"></el-radio>
          <el-radio label="最近的作战" value="5"></el-radio>

        </el-radio-group>
      </el-form-item>
      <el-form-item label="作战次数">
        <el-input v-model="temp.times"></el-input>
      </el-form-item>
      <el-form-item label="cron表达式">
        <el-input class="input" v-model="temp.day_of_week">
          <template slot="prepend">星期(0-6)</template>
        </el-input>
        <el-input class="input" v-model="temp.hour">
          <template slot="prepend">时</template>
        </el-input>
        <el-input class="input" v-model="temp.minute">
          <template slot="prepend">分</template>
        </el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="add_fight_job">添加</el-button>
      </el-form-item>
    </el-form>
  </el-card>

</template>

<script>
import {handle_suggestion_map_name} from '@/util/utils'
import {add_fight_job_service} from "@/service/JobService";

export default {
  name: "FightSchedulerAdd",
  data() {
    return {
      temp: {
        id: "",
        map_name: "",
        type: "",
        times: "",
        minute: "",
        hour: "",
        day_of_week: ""
      }
    }
  },
  computed: {},

  methods: {
    handle_suggestion_map_name(queryString, cb) {
      handle_suggestion_map_name(queryString, cb)
    },
    add_fight_job() {
      add_fight_job_service(this.temp)
    },
  }
}
</script>

<style scoped>

</style>