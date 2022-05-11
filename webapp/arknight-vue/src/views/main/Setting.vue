<template>
  <div>
    <h3>设置</h3>
    <el-card class="box-card">
      <div>
        <el-button @click="alt_config">
          编辑设置
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "SettingView",
  methods: {
    alt_config() {
      this.$http.get("/alt_config")
    }
  }
}
</script>

<style scoped>

</style>