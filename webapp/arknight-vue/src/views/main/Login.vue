<template>
  <el-form ref="user" :model="user" label-width="100px">
    <el-form-item label="用户名">
      <el-input v-model="user.userid"></el-input>
    </el-form-item>
    <el-form-item label="密码">
      <el-input v-model="user.password" type="password"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="login">登录</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import {login_submit_service,isLogin_service} from "@/service/StateService";
import {message_warning} from "@/util/utils";

export default {
  name: "LoginView",
  data() {
    return {
      user: {
        userid: "",
        password: ""
      }
    }
  },
  methods: {
    login() {
      login_submit_service(this.user)
      isLogin_service()
      if(this.$store.state.isLogin){
        this.$router.push({path:'/'})
      }else {
        message_warning('用户名或密码错误')
      }
    }
  }
}
</script>

<style scoped>
form {
  text-align: center;
  position: absolute; /*表单于页面居中*/
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

input[type=text], input[type=password] {
  background-color: white; /*正常状态样式*/
  color: black;
  border: none;
  border-radius: 20px;
  outline: none;
  text-align: center;
  height: 50px;
  width: 250px;
  margin: 5px;
}

input[type=button] {
  background-color: #45A0F2; /*正常状态样式*/
  color: white;
  border: none;
  border-radius: 20px;
  outline: none;
  text-align: center;
  height: 50px;
  width: 250px;
  margin: 5px;
}

input[type=text]:hover, input[type=password]:hover {
  outline: none; /*悬停时样式*/
  background-color: #65BCD6;
  color: white;
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.45), 0 6px 20px 0 rgba(0, 0, 0, 0.19); /*阴影*/
}

input[type=button]:hover {
  outline: none; /*悬停时样式*/
  background-color: #168DBE;
  color: white;
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.45), 0 6px 20px 0 rgba(0, 0, 0, 0.19); /*阴影*/
}
</style>