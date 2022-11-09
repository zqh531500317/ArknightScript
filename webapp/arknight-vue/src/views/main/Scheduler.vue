<template>
  <div>
    <h3>tips：</h3>
    <p>单次排班</p>
    <el-card class="box-card">
      <el-form ref="scheduler" :model="schedulerEntity" label-width="100px">

        <el-form-item label="排班文件相对路径">
          <el-input v-model="schedulerEntity.path"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="scheduler_submit">立即执行</el-button>
        </el-form-item>
      </el-form>
    </el-card>

  </div>
</template>

<script>
import {scheduler_service} from "@/service/RecruitService";
import {mapState} from "vuex";

export default {
  name: "SchedulerView",
  data() {
    return {
      schedulerEntity: {
        path: ""
      }
    }
  },
  computed: {
    ...mapState(['fight_state'])
  },
  methods: {
    scheduler_submit() {
      scheduler_service(this.schedulerEntity)
    }
  }
}
</script>

<style scoped>

</style>