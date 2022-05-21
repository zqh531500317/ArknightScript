<template>
  <div>
    <b>总览</b>
    <el-row :gutter="20">
      <el-col :span="12">
        <job-list></job-list>
      </el-col>
      <el-col :span="12">
        <keep-alive>
          <logger></logger>
        </keep-alive>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import logger from "@/components/Logger";
import jobList from "@/components/JobList";

export default {
  data() {
    return {
    }
  },
  components: {
    logger, jobList
  }
}
</script>

<style scoped>

</style>