<template>
  <div>
    <el-button @click="do_test_service">{{ fc[1] }}</el-button>

  </div>
</template>

<script>
import {test_service} from "@/service/TestService";

export default {
  name: "TestComponent",
  props: [
    'fc'
  ],
  methods: {
    do_test_service() {
      test_service({'fc':this.fc[0]})
    }
  }
}
</script>
<style scoped>

</style>