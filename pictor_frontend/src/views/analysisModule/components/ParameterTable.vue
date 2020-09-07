<template>
  <el-dialog
    title="参数方案"
    :visible.sync="dialogTableVisible"
    width="70%"
    @close="close"
  >
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
              <el-input v-model="queryForm.search" placeholder="方案名称" />
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
          prop="name"
          label="参数名称"
          sortable="custom"
        ></el-table-column>
        <el-table-column
          show-overflow-tooltip
          label="备注/描述"
          prop="remark"
          min-width="200"
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
            <el-button type="text" @click="handleDelete(scope.row)"
              >删除
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
      <parameter-edit
        ref="parameter-edit"
        @fetchParameterData="fetchData"
      ></parameter-edit>
    </div>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">关 闭</el-button>
    </div>
  </el-dialog>
</template>

<script>
import ParameterEdit from "./ParameterEdit";
import {
  getAnalysisParameterList,
  deleteAnalysisParameter,
  bulkDeleteAnalysisParameter,
} from "@/api/analysisParameter";

export default {
  name: "ParameterTable",
  filters: {},
  components: {
    ParameterEdit,
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
      dialogTableVisible: false,
      queryForm: {
        page: 1,
        page_size: 10,
        search: "",
        ordering: null,
      },
      module: {},
    };
  },
  created() {},
  beforeDestroy() {},
  mounted() {},
  methods: {
    showTable(module) {
      this.fetchData(module);
      this.module = module;
      this.dialogTableVisible = true;
    },
    close() {
      this.list = [];
      this.all_count = 0;
      this.selectRows = "";
      this.queryForm = {
        page: 1,
        page_size: 10,
        search: "",
        ordering: null,
      };
      this.module = {};
      this.dialogTableVisible = false;
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
      this.selectRows = val;
    },
    handleAdd() {
      this.$refs["parameter-edit"].showEdit(null, this.module);
    },
    handleEdit(row) {
      this.$refs["parameter-edit"].showEdit(row, this.module);
    },
    handleDelete(row) {
      if (row.id) {
        this.$baseConfirm("你确定要删除当前项吗", null, async () => {
          const data = await deleteAnalysisParameter(row.id);
          const messages = data.messages;
          this.$baseMessage(messages, "success");
          this.fetchData();
        });
      } else {
        if (this.selectRows.length > 0) {
          const ids = this.selectRows.map((item) => item.id);
          this.$baseConfirm("你确定要删除选中项吗", null, async () => {
            const data = await bulkDeleteAnalysisParameter({
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
    async fetchData(module) {
      if (module) {
        this.queryForm["module"] = module.id;
      }
      this.listLoading = true;
      const data = await getAnalysisParameterList(this.queryForm);
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
