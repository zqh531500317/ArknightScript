<template>
  <div>
    <h3>tips：</h3>
    <p>遇到高姿需手动选择</p>
    <p>请确保招聘许可和加急许可数量足够</p>
    <p>请确保第一个位置在待招聘状态</p>
    <el-card class="box-card">
      <el-form ref="recruit" :model="recruitEntity" label-width="100px">

        <el-form-item label="招募次数">
          <el-input v-model="recruitEntity.num"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="recruit_submit" v-if="this.fight_state!=='task'">立即执行</el-button>
          <el-button type="primary" @click="recruit_submit" v-if="this.fight_state==='task'" disabled>正在执行中</el-button>
        </el-form-item>
      </el-form>
    </el-card>

  </div>
</template>

<script>
import {recruit_service} from "@/service/RecruitService";
import {mapState} from "vuex";

export default {
  name: "RecruitView",
  data() {
    return {
      recruitEntity: {
        num: 0
      }
    }
  },
  computed: {
    ...mapState(['fight_state'])
  },
  methods: {
    recruit_submit() {
      recruit_service(this.recruitEntity)
    }
  }
}
</script>

<style scoped>

</style>