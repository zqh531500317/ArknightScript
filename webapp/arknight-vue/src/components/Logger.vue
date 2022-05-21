<template>
  <el-card class="box-card">
    <div style="height:500px;overflow:auto;" ref="logContent">
      <div v-for="(i,index) in logList" :key="index">
        {{ i }}
      </div>
    </div>
  </el-card>
</template>

<script>


import {mapMutations, mapState} from "vuex";

export default {
  name: "loggerComponent",
  methods: {
    ...mapMutations(['set_logList']),
    scroll_logContent_to_bottom() {
      this.$nextTick(() => {
        this.$refs.logContent.scrollTop = this.$refs.logContent.scrollHeight;
      })
    }
  },
  computed: {
    ...mapState(['logList']),

  },
  watch: {
    logList: {//深度监听，可监听到对象、数组的变化
      handler() {
        this.scroll_logContent_to_bottom()
      },
      deep: true //true 深度监听
    }
  },

  mounted() {
    this.scroll_logContent_to_bottom()
  }
}
</script>

<style scoped>

</style>