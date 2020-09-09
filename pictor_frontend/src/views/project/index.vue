<template>
  <div class="table-container">
    <vab-query-form>
      <vab-query-form-left-panel>
        <el-button
          v-if="project_permissions.add"
          icon="el-icon-plus"
          type="primary"
          @click="handleAdd"
          >添加
        </el-button>
        <el-button
          v-if="project_permissions.delete"
          icon="el-icon-delete"
          type="danger"
          @click="handleDelete"
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
              placeholder="项目编号/项目名称"
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
      ref="projectTable"
      v-loading="listLoading"
      :data="list"
      :element-loading-text="elementLoadingText"
      @selection-change="setSelectRows"
      @sort-change="tableSortChange"
    >
      <el-table-column
        show-overflow-tooltip
        type="selection"
        width="55"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="项目编号"
        prop="serial_number"
        sortable="custom"
      >
      </el-table-column>
      <el-table-column
        show-overflow-tooltip
        prop="name"
        label="项目名称"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="项目描述/备注"
        prop="remark"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="创建者"
        prop="creator.nickname"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="创建时间"
        prop="created_time"
        width="200"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="操作"
        width="180px"
        fixed="right"
      >
        <template slot-scope="scope">
          <el-button
            v-if="project_permissions.edit"
            type="text"
            @click="handleEdit(scope.row)"
            >编辑
          </el-button>
          <el-button
            v-if="project_permissions.delete"
            type="text"
            @click="handleDelete(scope.row)"
            >删除
          </el-button>
          <el-button
            v-if="project_permissions.manage"
            type="text"
            @click="handleMange(scope.row)"
            >管理
          </el-button>
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
    <project-edit ref="edit" @listEvent="fetchData"></project-edit>
    <project-manage ref="manage" @listEvent="fetchData"></project-manage>
  </div>
</template>

<script>
import ProjectEdit from "./components/ProjectEdit";
import ProjectManage from "./components/ProjectManage";
import {
  getProjectList,
  deleteProject,
  bulkDeleteProject,
} from "@/api/project";
import { getActionPermission } from "@/api/actionPermission";
export default {
  name: "ProjectTable",
  components: {
    ProjectEdit,
    ProjectManage,
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
      project_permissions: {},
      queryForm: {
        page: 1,
        page_size: 10,
        search: "",
        ordering: null,
      },
    };
  },
  created() {
    this.fetchPermission();
    this.fetchData();
  },
  beforeDestroy() {},
  mounted() {},
  methods: {
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
      console.log("handleAdd");
      this.$refs["edit"].showEdit();
    },
    handleEdit(row) {
      this.$refs["edit"].showEdit(row);
    },
    handleMange(row) {
      this.$refs["manage"].showMange(row);
    },
    handleDelete(row) {
      if (row.id) {
        this.$baseConfirm("你确定要删除当前项吗", null, async () => {
          const data = await deleteProject(row.id);
          const messages = data.messages;
          this.$baseMessage(messages, "success");
          this.fetchData();
        });
      } else {
        if (this.selectRows.length > 0) {
          const ids = this.selectRows.map((item) => item.id);
          this.$baseConfirm("你确定要删除选中项吗", null, async () => {
            const data = await bulkDeleteProject({ deleted_objects: ids });
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
    async fetchPermission() {
      const data = await getActionPermission({ permission_type: "project" });
      this.project_permissions = data.results.project;
    },
    async fetchData() {
      this.listLoading = true;
      const data = await getProjectList(this.queryForm);
      this.list = data.results;
      this.all_count = data.all_count;
      setTimeout(() => {
        this.listLoading = false;
      }, 500);
    },
  },
};
</script>
