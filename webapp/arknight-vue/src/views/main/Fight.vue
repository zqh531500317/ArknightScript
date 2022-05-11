<template>
  <div>
    <h3>tips：</h3>
    <p>地图名称(区分大小写)</p>
    <p>地图类型(已支持主线，资源收集，剿灭，未适配作战)</p>
    <p>剿灭无需输地图名称，会自动判断需要打的次数</p>
    <p>未适配作战(需手动进入到作战前的界面)</p>
    <p>参考:</p>
    <p>CA = 技能书本&emsp;&emsp;LS = 经验本&emsp;&emsp;AP = 红票本&emsp;&emsp;SK = 碳本&emsp;&emsp;CE = 龙门币本</p>
    <p>PR-A = 医疗重装芯片&emsp;&emsp;PR-B = 狙击术士芯片&emsp;&emsp;PR-C = 辅助先锋芯片&emsp;&emsp;PR-D = 近卫特种芯片</p>
    <p>更新时间2021.10.25</p>
    <el-link href="https://aog.wiki/" target="_blank">更多内容：https://aog.wiki/</el-link>

    <el-card class="box-card">
      <el-form ref="fight" :model="fight" label-width="100px">
        <el-form-item label="地图名称">
          <el-autocomplete
              class="inline-input"
              v-model="fight.name"
              :fetch-suggestions="handle_suggestion_map_name"
              placeholder="请输入内容"
          ></el-autocomplete>
        </el-form-item>
        <el-form-item label="地图类型">
          <el-radio-group v-model="fight.type">
            <el-radio label="主线" value="1"></el-radio>
            <el-radio label="资源收集" value="2"></el-radio>
            <el-radio label="剿灭" value="3"></el-radio>
            <el-radio label="活动" value="5"></el-radio>
            <el-radio label="未适配作战" value="4"></el-radio>
            <el-radio label="最近的作战" value="6"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="作战次数">
          <el-input v-model="fight.times"></el-input>
        </el-form-item>
        <el-form-item label="附加选项">
          <el-checkbox v-model="fight.use_medicine">使用理智药</el-checkbox>
          <el-input v-model="fight.medicine_num" placeholder="0"></el-input>
          <el-checkbox v-model="fight.use_stone">碎石</el-checkbox>
          <el-input v-model="fight.stone_num" placeholder="0"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fight_submit" v-if="this.fight_state!=='running'">立即执行</el-button>
          <el-button type="info" @click="fight_submit" v-if="this.fight_state==='running'" disabled>正在作战</el-button>
        </el-form-item>
      </el-form>
    </el-card>

  </div>
</template>

<script>
import {handle_suggestion_map_name} from '@/util/utils'
import {fight_submit} from "@/service/FightService";
import {mapState} from "vuex";
export default {
  name: "FightView",
  methods: {
    handle_suggestion_map_name(queryString, cb) {
      handle_suggestion_map_name(queryString, cb)
    },
    fight_submit() {
      fight_submit(this.fight)
    }
  },
  computed:{
    ...mapState(['fight_state'])
  },
  data() {
    return {
      fight: {
        name: '',
        type: "",
        times: "",
        use_medicine: false,
        medicine_num: 0,
        use_stone: false,
        stone_num: 0
      }
    }
  }
}
</script>

<style scoped>

</style>