<template>
  <div id="app">
    <el-container style="border: 1px solid #eee" direction="vertical">
      <my_header></my_header>
      <el-container>
        <my_aside></my_aside>
        <my_main></my_main>
      </el-container>
    </el-container>
  </div>
</template>

<script>

import my_header from '@/views/Header.vue'
import my_aside from '@/views/Aside.vue'
import my_main from '@/views/Main.vue'
import init from "@/service/init"
init()

export default {
  name: 'App',
  components: {my_header, my_aside, my_main},

  sockets: {
    connect() {
      console.log('socket connected')
    },
    disconnect() {
      console.log("断开链接");
    },
    dcenter(data) {
      console.log(data)
      let t = data.data
      if (t) {
        this.$store.commit('set_logList', t)
      }
      console.log(t)
    },
  }
}
</script>
<style>
.pad {
  padding: 5px;
  margin-bottom: 5px;
}

.input {
  width: 200px;
  float: left;
  margin-right: 10px
}

.line {
  margin: 10px;
  border-bottom: 1px solid #ccc

}
body{
  font-size: 1vw;
}
</style>
