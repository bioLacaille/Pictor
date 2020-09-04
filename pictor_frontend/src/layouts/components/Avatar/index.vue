<template>
  <el-dropdown @command="handleCommand">
    <span class="avatar-dropdown">
      <el-avatar class="user-avatar" :src="avatar"></el-avatar>
      <div class="user-name">
        {{ userName }}<i class="el-icon-arrow-down el-icon--right"></i>
      </div>
    </span>

    <el-dropdown-menu slot="dropdown">
      <el-dropdown-item command="workZone">
        <af-icon :icon="['fas', 'network-wired']"></af-icon>
        工作区
      </el-dropdown-item>
      <el-dropdown-item command="personalCenter">
        <af-icon :icon="['fas', 'user']"></af-icon>
        个人中心
      </el-dropdown-item>
      <el-dropdown-item command="logout" divided>
        <af-icon :icon="['fas', 'sign-out-alt']"></af-icon>
        退出登录
      </el-dropdown-item>
    </el-dropdown-menu>
  </el-dropdown>
</template>

<script>
/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 右上角个人用户展示内容
 **/
import { mapGetters } from "vuex";
import { recordRoute } from "@/config/settings";

export default {
  name: "Avatar",
  computed: {
    ...mapGetters({
      avatar: "user/avatar",
      userName: "user/userName",
    }),
  },
  methods: {
    handleCommand(command) {
      switch (command) {
        case "logout":
          this.logout();
          break;
        case "personalCenter":
          this.personalCenter();
          break;
        case "workZone":
          this.workZone();
          break;
      }
    },
    workZone() {
      this.$router.push("/workzones");
    },
    personalCenter() {
      this.$router.push("/personalCenter/personalCenter");
    },
    logout() {
      this.$baseConfirm(
        "您确定要退出" + this.$baseTitle + "吗?",
        null,
        async () => {
          await this.$store.dispatch("user/logout");
          if (recordRoute) {
            const fullPath = this.$route.fullPath;
            await this.$router.push(`/login?redirect=${fullPath}`);
          } else {
            await this.$router.push("/login");
          }
        }
      );
    },
  },
};
</script>
<style lang="scss" scoped>
.avatar-dropdown {
  padding: 0;
  height: 50px;
  display: flex;
  align-items: center;
  align-content: center;
  justify-items: center;
  justify-content: center;

  .user-avatar {
    cursor: pointer;
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }

  .user-name {
    margin-left: 5px;
    position: relative;
    margin-left: 5px;
    font-weight: 600;
    cursor: pointer;
  }
}
</style>
