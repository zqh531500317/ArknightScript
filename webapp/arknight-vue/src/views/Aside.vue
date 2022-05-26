<template>
  <el-aside width="200px">
        <h5>默认颜色</h5>
        <el-menu
            :default-active="page"
            :default-openeds="openeds"
            :collapse="isCollapse"
            router>

          <el-menu-item index="/">
            <i class="el-icon-s-home"></i>
            <span slot="title">总览</span>
          </el-menu-item>
          <el-menu-item index="/setting">
            <i class="el-icon-setting"></i>
            <span slot="title">设置</span>
          </el-menu-item>
          <el-menu-item index="/fight">
            <i class="el-icon-right"></i>
            <span slot="title">作战</span>
          </el-menu-item>

          <el-submenu index="4">
            <template slot="title">
              <i class="el-icon-date"></i>
              <span slot="title">自动化</span>
            </template>
            <el-menu-item index="/mainScheduler">收获</el-menu-item>
            <el-menu-item index="/fightScheduler">战斗</el-menu-item>
          </el-submenu>
          <el-menu-item index="/recruit">
            <i class="el-icon-right"></i>
            <span slot="title">公开招募</span>
          </el-menu-item>
          <el-menu-item index="/test">
            <i class="el-icon-right"></i>
            <span slot="title">测试</span>
          </el-menu-item>
        </el-menu>
  </el-aside>

</template>

<script>
export default {
  name: "AsideView",
  data() {
    return {
      isCollapse: false,
      openeds: ['4'],
      page: "/"
    }
  }
}
</script>

<style scoped>

</style>