<template>
  <div>
    <div>
      <el-row :gutter="10">
        <el-col :span="12" v-for="(job,index) in this.$store.state.fight_jobs" :key="index">
          <fightSchedulerCard :job="job"></fightSchedulerCard>
        </el-col>
      </el-row>
    </div>
    <fightSchedulerAdd></fightSchedulerAdd>

  </div>
</template>

<script>
import fightSchedulerCard from '@/components/FightSchedulerCard'
import fightSchedulerAdd from '@/components/FightSchedulerAdd'
import {mapState} from "vuex";

export default {
  name: "FightSchedulerView",
  data() {
    return {}
  },
  computed: {
    ...mapState(['fight_jobs']),
  },
  methods: {

  },
  components: {
    fightSchedulerCard, fightSchedulerAdd
  }
}
</script>

<style scoped>

</style>