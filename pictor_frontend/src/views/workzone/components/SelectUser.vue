<template>
  <el-dialog
    title="选择成员(todo:滚动条与搜索框)"
    :visible.sync="dialogFormVisible"
    width="80%"
    @close="close"
  >
    <div class="components-container board">
      <user-draggable
        :key="0"
        :draggable-type="0"
        :instance-id="instance_id"
        :list="select_users"
        :group="group"
        :scroll-sensitivity="20"
        class="draggable todo"
        header-text="可选成员"
        @refreshMembers="refreshMembers"
      />
      <user-draggable
        v-for="(value, propertyName, index) in member_types"
        :key="propertyName"
        :draggable-type="parseInt(propertyName)"
        :instance-id="instance_id"
        :list="members[parseInt(propertyName)]"
        :group="group"
        class="draggable"
        :class="class_styles[index]"
        :header-text="value.desc"
        @refreshMembers="refreshMembers"
      />
    </div>
  </el-dialog>
</template>
<script>
import UserDraggable from "./UserDraggable";
import { getWorkZoneMemberList, getWorkZoneMemberTypes } from "@/api/workzone";
// todo:滚动条与搜索框
export default {
  name: "SelectUser",
  components: {
    UserDraggable,
  },
  data() {
    return {
      dialogFormVisible: false,
      group: "users",
      instance_id: null,
      select_users: [],
      member_types: {},
      members: {},
      class_styles: [
        "guests",
        "users",
        "maintainers",
        "admins",
        "admins",
        "admins",
      ],
    };
  },
  created() {},
  methods: {
    showSelectUser(row) {
      this.instance_id = row.id;
      this.dialogFormVisible = true;
      this.initMembersForm();
      this.fetchSelectUsers();
    },
    close() {
      this.instance_id = null;
      this.select_users = [];
      this.members = {};
      this.dialogFormVisible = false;
    },
    async fetchSelectUsers() {
      this.select_users = [];
      const data = await getWorkZoneMemberList(this.instance_id, {
        filter_not_members: true,
      });
      const { messages, results } = data;
      for (let i = 0; i < results.length; i++) {
        this.select_users.push({
          id: results[i].id,
          name: `${results[i].nickname}\(${results[i].username}\)`,
        });
      }
    },
    async initMembersForm() {
      const data = await getWorkZoneMemberTypes({ mixing: true });
      const { messages, results } = await data;
      for (let i = 0; i < results.length; i++) {
        this.member_types[results[i].key] = {
          value: results[i].value,
          desc: results[i].desc,
        };
        this.fetchMembers(results[i].key);
      }
    },
    async fetchMembers(level) {
      const data = await getWorkZoneMemberList(this.instance_id, {
        level: level,
      });
      this.members[level] = [];
      const { messages, results } = data;
      for (let i = 0; i < results.length; i++) {
        this.members[level].push({
          id: results[i].user.id,
          name: `${results[i].user.nickname}\(${results[i].user.username}\)`,
        });
      }
      // 强制重新渲染视图
      this.$forceUpdate();
    },
    refreshMembers() {
      const _that = this;
      this.fetchSelectUsers();
      Object.keys(this.members).forEach(function (key) {
        _that.fetchMembers(key);
      });
    },
  },
};
</script>
<style lang="scss">
.board {
  /*width: 1000px;*/
  margin-left: 10px;
  display: flex;
  justify-content: space-around;
  flex-direction: row;
  align-items: flex-start;
}
.draggable {
  &.todo {
    .board-column-header {
      background: #4a9ff9;
    }
  }
  &.guests {
    .board-column-header {
      background: #f9944a;
    }
  }
  &.users {
    .board-column-header {
      background: #2ac06d;
    }
  }
  &.maintainers {
    .board-column-header {
      background: lightblue;
    }
  }
  &.admins {
    .board-column-header {
      background: lightcoral;
    }
  }
}
</style>
