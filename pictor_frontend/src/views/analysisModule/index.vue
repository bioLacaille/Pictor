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
              placeholder="模块名称/模块版本"
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
        label="模块来源"
        prop="module_type"
        sortable="custom"
      >
        <template slot-scope="scope">
          <el-tag :type="moduleTypeTagFilter(scope.row.module_type)">{{
            moduleTypeNameFilter(scope.row.module_type)
          }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        show-overflow-tooltip
        prop="name"
        label="模块名称"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        prop="version"
        label="版本号"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="状态"
        prop="status"
        sortable="custom"
      >
        <template slot-scope="scope">
          <el-tag :type="moduleStatusTagFilter(scope.row.status)">{{
            moduleStatusNameFilter(scope.row.status)
          }}</el-tag>
        </template>
      </el-table-column>
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
          <el-button type="text" @click="handleEdit(scope.row)"
            >编辑
          </el-button>
          <el-button type="text" @click="handleParameter(scope.row)"
            >参数方案
          </el-button>
          <el-dropdown>
            <el-button type="text" size="small"
              >更多<i class="el-icon-arrow-down el-icon--right"></i
            ></el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item @click.native="handleDelete(scope.row)"
                >删除</el-dropdown-item
              >
              <el-dropdown-item
                v-if="
                  scope.row.status === 10 ||
                  scope.row.status === 30 ||
                  scope.row.status === 50
                "
                @click.native="handleInstall(scope.row)"
                >安装</el-dropdown-item
              >
              <el-dropdown-item
                v-if="scope.row.status === 40"
                @click.native="handleUnInstall(scope.row)"
                >卸载</el-dropdown-item
              >
              <el-dropdown-item
                v-if="scope.row.status === 20"
                @click.native="handleStopInstall(scope.row)"
                >停止安装</el-dropdown-item
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
    <analysis-module-edit
      ref="edit"
      @listEvent="fetchData"
    ></analysis-module-edit>
    <parameter-table ref="parameter"></parameter-table>
  </div>
</template>

<script>
import AnalysisModuleEdit from "./components/AnalysisModuleEdit";
import ParameterTable from "./components/ParameterTable";
import {
  getAnalysisModuleList,
  deleteAnalysisModule,
  bulkDeleteAnalysisModule,
  getAnalysisModuleTypes,
  getAnalysisModuleStatus,
  installAnalysisModule,
  uninstallAnalysisModule,
  stopInstallAnalysisModule,
} from "@/api/analysisModule";

export default {
  name: "AnalysisModuleTable",
  filters: {},
  components: {
    AnalysisModuleEdit,
    ParameterTable,
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
      tagTypeList: [
        "",
        "success",
        "info",
        "warning",
        "danger",
        "grey",
        "yellow",
      ],
      moduleTypeMap: {},
      moduleStatusMap: {},
      moduleTypeTagMap: {},
      moduleStatusTagMap: {},
    };
  },
  created() {
    this.getModuleTypeFilter();
    this.getModuleStatusFilter();
    this.$nextTick(function () {
      this.fetchData();
    });
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
      this.selectRows = val;
    },
    handleAdd() {
      console.log("handleAdd");
      this.$refs["edit"].showEdit();
    },
    handleEdit(row) {
      this.$refs["edit"].showEdit(row);
    },
    handleParameter(row) {
      this.$refs["parameter"].showTable(row);
    },
    handleDelete(row) {
      if (row.id) {
        this.$baseConfirm("你确定要删除当前项吗", null, async () => {
          const data = await deleteAnalysisModule(row.id);
          const messages = data.messages;
          this.$baseMessage(messages, "success");
          this.fetchData();
        });
      } else {
        if (this.selectRows.length > 0) {
          const ids = this.selectRows.map((item) => item.id);
          this.$baseConfirm("你确定要删除选中项吗", null, async () => {
            const data = await bulkDeleteAnalysisModule({
              deleted_objects: ids,
            });
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
    handleInstall(row) {
      this.$baseConfirm("你确定要安装当前项吗", null, async () => {
        const data = await installAnalysisModule(row.id);
        const messages = data.messages;
        this.$baseMessage(messages, "success");
        this.fetchData();
      });
    },
    handleUnInstall(row) {
      this.$baseConfirm("你确定要卸载当前项吗", null, async () => {
        const data = await uninstallAnalysisModule(row.id);
        const messages = data.messages;
        this.$baseMessage(messages, "success");
        this.fetchData();
      });
    },
    handleStopInstall(row) {
      this.$baseConfirm("你确定要停止安装当前项吗", null, async () => {
        const data = await stopInstallAnalysisModule(row.id);
        const messages = data.messages;
        this.$baseMessage(messages, "success");
        this.fetchData();
      });
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
    moduleTypeTagFilter(val) {
      return this.moduleTypeTagMap[val];
    },
    moduleTypeNameFilter(val) {
      return this.moduleTypeMap[val];
    },
    moduleStatusTagFilter(val) {
      return this.moduleStatusTagMap[val];
    },
    moduleStatusNameFilter(val) {
      return this.moduleStatusMap[val];
    },
    async getModuleTypeFilter() {
      const data = await getAnalysisModuleTypes();
      for (let i = 0; i < data.results.length; i++) {
        this.moduleTypeMap[data.results[i].key] = data.results[i].value;
        this.moduleTypeTagMap[data.results[i].key] = this.tagTypeList[i];
      }
      // 强制重新渲染视图
      this.$forceUpdate();
    },
    async getModuleStatusFilter() {
      const status_data = await getAnalysisModuleStatus();
      for (let i = 0; i < status_data.results.length; i++) {
        this.moduleStatusMap[status_data.results[i].key] =
          status_data.results[i].value;
        this.moduleStatusTagMap[status_data.results[i].key] = this.tagTypeList[
          i
        ];
      }
      // 强制重新渲染视图
      this.$forceUpdate();
    },
    async fetchData() {
      this.listLoading = true;
      const data = await getAnalysisModuleList(this.queryForm);
      this.list = data.results;
      this.all_count = data.all_count;
      setTimeout(() => {
        this.listLoading = false;
        // 强制重新渲染视图
        this.$forceUpdate();
      }, 500);
    },
  },
};
</script>
