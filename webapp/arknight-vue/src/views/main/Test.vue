<template>
  <div>
    <h3>测试</h3>
    <el-row>
      <el-col :span="10">
        <div v-for="(fc,index) in fcList" :key="index">
          <TestComponent :fc="fc"></TestComponent>
        </div>
      </el-col>
      <el-col :span="14">
        <logger></logger>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import TestComponent from "@/components/TestComponent";
import {testlist} from "@/api/test";
import logger from "@/components/Logger";

export default {
  name: "TestView",
  data() {
    return {
      fcList: []
    }
  },
  components: {
    TestComponent, logger
  },
  created() {
    testlist().then((e) => {
      this.fcList = e
    })
  }
}
</script>

<style scoped>

</style>