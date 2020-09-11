<template>
  <div class="table-container">
    <vab-query-form>
      <vab-query-form-left-panel>
        <el-button icon="el-icon-plus" type="primary" @click="handleAdd"
          >添加
        </el-button>
        <el-button icon="el-icon-delete" type="danger" @click="handleDelete"
          >删除
        </el-button>
      </vab-query-form-left-panel>
      <vab-query-form-right-panel>
        <el-form
          ref="form"
          :model="queryForm"
          :inline="true"
          @submit.native.prevent
        >
          <el-form-item>
            <el-input
              v-model="queryForm.search"
              placeholder="用户账号/昵称/邮箱/性别/电话/职称"
            />
          </el-form-item>
          <el-form-item>
            <el-button
              icon="el-icon-search"
              type="primary"
              native-type="submit"
              @click="handleQuery"
              >查询
            </el-button>
          </el-form-item>
        </el-form>
      </vab-query-form-right-panel>
    </vab-query-form>

    <el-table
      ref="userTable"
      v-loading="listLoading"
      :data="list"
      :element-loading-text="elementLoadingText"
      @selection-change="setSelectRows"
      @sort-change="tableSortChange"
    >
      >
      <el-table-column
        show-overflow-tooltip
        type="selection"
        width="55"
      ></el-table-column>
      <el-table-column show-overflow-tooltip prop="is_active" label="是否可用">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.is_active" size="medium" type="success">
            可用
          </el-tag>
          <el-tag v-else size="medium" type="info"> 禁用 </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        show-overflow-tooltip
        prop="related_files_count"
        label="用户角色"
      >
        <template slot-scope="scope">
          <el-tag size="medium" :type="filerLevelColor(scope.row.role_level)">
            {{ scope.row.role }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="用户账号"
        prop="username"
        sortable="custom"
      >
      </el-table-column>
      <el-table-column
        show-overflow-tooltip
        prop="nickname"
        label="昵称"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        prop="email"
        label="邮箱"
        sortable="custom"
      ></el-table-column>
      <!--      <el-table-column-->
      <!--        show-overflow-tooltip-->
      <!--        prop="gender"-->
      <!--        label="性别"-->
      <!--        sortable="custom"-->
      <!--      ></el-table-column>-->
      <!--      <el-table-column-->
      <!--        show-overflow-tooltip-->
      <!--        prop="phone"-->
      <!--        label="电话"-->
      <!--        sortable="custom"-->
      <!--      ></el-table-column>-->
      <!--      <el-table-column-->
      <!--        show-overflow-tooltip-->
      <!--        prop="title"-->
      <!--        label="职称"-->
      <!--        sortable="custom"-->
      <!--      ></el-table-column>-->
      <el-table-column
        show-overflow-tooltip
        label="创建时间"
        prop="created_time"
        width="200"
        sortable="custom"
      ></el-table-column>
      <el-table-column show-overflow-tooltip label="操作" fixed="right">
        <template slot-scope="scope">
          <el-button type="text" @click="handleEdit(scope.row)"
            >编辑
          </el-button>
          <el-button type="text" @click="handleDelete(scope.row)"
            >删除
          </el-button>
          <el-dropdown>
            <el-button type="text" size="small"
              >更多<i class="el-icon-arrow-down el-icon--right"></i
            ></el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item
                v-if="!scope.row.is_active"
                @click.native="handleActivation(scope.row, true)"
                >启用</el-dropdown-item
              >
              <el-dropdown-item
                v-else
                @click.native="handleActivation(scope.row, false)"
                >禁用</el-dropdown-item
              >
              <el-dropdown-item @click.native="handleResetPassword(scope.row)"
                >重置密码</el-dropdown-item
              >
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      :background="background"
      :current-page="queryForm.page"
      :layout="layout"
      :page-size="queryForm.page_size"
      :total="all_count"
      @current-change="handleCurrentChange"
      @size-change="handleSizeChange"
    ></el-pagination>
    <user-edit ref="edit" @listEvent="fetchData"></user-edit>
    <reset-pawword ref="reset_password" @listEvent="fetchData"></reset-pawword>
  </div>
</template>

<script>
import UserEdit from "./components/UserEdit";
import ResetPawword from "./components/ResetPawword";
import {
  getUserList,
  deleteUser,
  bulkDeleteUser,
  activationUser,
} from "@/api/user";

export default {
  name: "UserTable",
  components: {
    UserEdit,
    ResetPawword,
  },
  data() {
    return {
      list: [],
      listLoading: true,
      layout: "total, sizes, prev, pager, next, jumper",
      all_count: 0,
      background: true,
      selectRows: "",
      elementLoadingText: "正在加载...",
      queryForm: {
        page: 1,
        page_size: 10,
        search: "",
        ordering: null,
      },
    };
  },
  created() {
    this.fetchData();
  },
  beforeDestroy() {},
  mounted() {},
  methods: {
    filerLevelColor(level) {
      if (level === 10) {
        return "success";
      } else if (level === 20) {
        return "info";
      } else if (level === 30) {
        return "warning";
      } else if (level === 40) {
        return "danger";
      } else {
        return "success";
      }
    },
    tableSortChange(data) {
      const { prop, order } = data;
      if (order === "ascending" || order === null) {
        this.queryForm.ordering = prop;
      } else {
        this.queryForm.ordering = `-${prop}`;
      }
      this.fetchData();
    },
    setSelectRows(val) {
      console.log(val);
      this.selectRows = val;
    },
    handleAdd() {
      this.$refs["edit"].showEdit();
    },
    handleEdit(row) {
      this.$refs["edit"].showEdit(row);
    },
    handleResetPassword(row) {
      this.$refs["reset_password"].showEdit(row);
    },
    handleDelete(row) {
      if (row.id) {
        this.$baseConfirm("你确定要删除此用户吗", null, async () => {
          const data = await deleteUser(row.id);
          const messages = data.messages;
          this.$baseMessage(messages, "success");
          this.fetchData();
        });
      } else {
        if (this.selectRows.length > 0) {
          const ids = this.selectRows.map((item) => item.id);
          this.$baseConfirm("你确定要删除选中用户吗", null, async () => {
            const data = await bulkDeleteUser({ deleted_objects: ids });
            const messages = data.messages;
            this.$baseMessage(messages, "success");
            this.fetchData();
          });
        } else {
          this.$baseMessage("未选中任何行", "error");
          return false;
        }
      }
    },
    handleSizeChange(val) {
      this.queryForm.page_size = val;
      this.fetchData();
    },
    handleCurrentChange(val) {
      this.queryForm.page = val;
      this.fetchData();
    },
    handleQuery() {
      this.queryForm.page = 1;
      this.fetchData();
    },
    handleActivation(row, active) {
      console.log("handleActivation active", active);
      if (row.id) {
        let msg = "启用";
        if (!active) {
          msg = "禁用";
        }
        this.$baseConfirm(`你确定要${msg}此用户吗?`, null, async () => {
          const data = await activationUser(row.id, { active: false });
          const messages = data.messages;
          this.$baseMessage(messages, "success");
          this.fetchData();
        });
      } else {
        this.$baseMessage("未选中任何行", "error");
        return false;
      }
    },
    async fetchData() {
      this.listLoading = true;
      const data = await getUserList(this.queryForm);
      this.list = data.results;
      this.all_count = data.all_count;
      setTimeout(() => {
        this.listLoading = false;
      }, 500);
    },
  },
};
</script>
