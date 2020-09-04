<template>
  <div>
    <el-card class="dk-box-card-main" shadow="never">
      <dk-list-key-value
        class="dk-normal-list-header"
        :xs="24"
        :sm="8"
        :list="statistics"
      ></dk-list-key-value>
    </el-card>
    <el-card class="dk-box-card-main" shadow="never">
      <!-- 搜索表单 -->
      <el-form
        action="javascript:void(0);"
        :inline="true"
        :model="queryForm"
        size="small"
        class="dk-search-form"
        @submit.native="submitSearchForm"
      >
        <el-form-item key="status" prop="status">
          <el-radio-group
            v-model="queryForm.status"
            @change="submitSelectStatus"
          >
            <el-radio-button key="" label="">全部</el-radio-button>
            <el-radio-button
              v-for="(item, key) in statusOptions"
              :key="key"
              :label="key"
              >{{ item }}</el-radio-button
            >
          </el-radio-group>
        </el-form-item>
        <el-form-item key="title" prop="title">
          <el-input v-model="queryForm.search" placeholder="请输入分析编号">
            <el-button
              slot="append"
              icon="el-icon-search"
              native-type="submit"
            ></el-button>
          </el-input>
        </el-form-item>
      </el-form>
      <!-- 标准列表 -->
      <el-button
        class="dk-btn-block is-ghost"
        size="medium"
        plain
        type="primary"
        icon="el-icon-plus"
        @click="handleAddAnalysis"
        >添加</el-button
      >
      <el-table class="dk-normal-list" :data="listData" :show-header="true">
        <el-table-column min-width="250">
          <template slot-scope="scope">
            <dk-list :is-single-data="true" :list="scope.row"></dk-list>
          </template>
        </el-table-column>
        <el-table-column width="150">
          <template slot-scope="scope">
            <span class="dk-normal-list-header">项目</span>
            <p v-if="scope.row.project">
              {{ scope.row.project.serial_number }}({{
                scope.row.project.name
              }})
            </p>
            <p v-else>无</p>
          </template>
        </el-table-column>
        <el-table-column width="150">
          <template slot-scope="scope">
            <span class="dk-normal-list-header">模块</span>
            <p v-if="scope.row.analysis_module">
              {{ scope.row.analysis_module.name }}
            </p>
            <p v-else>无</p>
          </template>
        </el-table-column>
        <el-table-column width="150">
          <template slot-scope="scope">
            <span class="dk-normal-list-header">模块版本</span>
            <p v-if="scope.row.analysis_module">
              {{ scope.row.analysis_module.version }}
            </p>
            <p v-else>无</p>
          </template>
        </el-table-column>
        <el-table-column width="100">
          <template slot-scope="scope">
            <!--            <span class="dk-normal-list-header">状态</span>-->
            <el-tag :type="StatusTagFilter(scope.row.status)">
              <p>{{ statusOptions[scope.row.status] }}</p>
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column width="160">
          <template slot-scope="scope">
            <span class="dk-normal-list-header">开始时间</span>
            <p>{{ scope.row.started_time }}</p>
          </template>
        </el-table-column>
        <el-table-column width="160">
          <template slot-scope="scope">
            <span class="dk-normal-list-header">结束时间</span>
            <p>{{ scope.row.finished_time }}</p>
          </template>
        </el-table-column>
        <el-table-column width="200">
          <template slot-scope="scope">
            <el-progress :percentage="scope.row.progress"></el-progress>
          </template>
        </el-table-column>
        <el-table-column fixed="right" width="120">
          <template slot-scope="scope">
            <el-button
              type="text"
              size="small"
              @click="handleShowAnalysis(scope.row)"
              >查看</el-button
            >
            <el-divider direction="vertical"></el-divider>
            <el-dropdown>
              <el-button type="text" size="small"
                >更多<i class="el-icon-arrow-down el-icon--right"></i
              ></el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native="handleEditAnalysis(scope.row)"
                  >编辑</el-dropdown-item
                >
                <el-dropdown-item @click.native="handleDelete(scope.row)"
                  >删除</el-dropdown-item
                >
                <el-dropdown-item @click.native="handleStart(scope.row)"
                  >启动</el-dropdown-item
                >
                <el-dropdown-item @click.native="handleStop(scope.row)"
                  >停止</el-dropdown-item
                >
                <el-dropdown-item @click.native="handleContinueRun(scope.row)"
                  >继续运行</el-dropdown-item
                >
                <el-dropdown-item @click.native="handleReset(scope.row)"
                  >重置</el-dropdown-item
                >
                <el-dropdown-item>克隆(todo)</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页 -->
      <el-pagination
        class="dk-pagination"
        background
        :current-page="queryForm.page"
        :page-sizes="[10, 50, 100, 200, 300, 400]"
        :page-size="queryForm.page_size"
        :layout="layout"
        :pager-count="5"
        :total="all_count"
        @size-change="handlePageSizeChange"
        @current-change="handleCurrentChange"
      >
      </el-pagination>
    </el-card>
    <add-analysis ref="add" @fetchData="fetchData"></add-analysis>
    <show-analysis ref="show" @fetchData="fetchData"></show-analysis>
  </div>
</template>

<script>
import DkListKeyValue from "@/components/DKComponents/list/DkListKeyValue"; // 导入
import DkList from "@/components/DKComponents/list/DkList"; // 导入
import {
  getAnalysisList,
  getAnalysisStatusList,
  getAnalysisStatistics,
  deleteAnalysis,
  startAnalysis,
  stopAnalysis,
  continueRunAnalysis,
  resetAnalysis,
} from "@/api/analysis";
import AddAnalysis from "./components/AddAnalysis";
import ShowAnalysis from "./components/ShowAnalysis";
export default {
  name: "Analysis",
  components: {
    AddAnalysis,
    ShowAnalysis,
    DkListKeyValue,
    DkList,
  },
  data() {
    return {
      statistics: [
        { key: "总任务数", value: "0" },
        { key: "本月任务平均处理时间", value: "0" },
        { key: "本月完成任务数", value: "0" },
      ],
      statusOptions: {},
      listData: [],
      layout: "total, sizes, prev, pager, next, jumper",
      all_count: 0,
      queryForm: {
        page: 1,
        page_size: 10,
        search: "",
        status: "",
        ordering: null,
      },
    };
  },
  created() {
    this.fetchAnalysisStatus();
    this.fetchAnalysisStatistics();
    this.fetchData();
  },
  methods: {
    submitSearchForm() {
      this.fetchData();
    },
    submitSelectStatus(val) {
      this.queryForm.status = val;
      this.fetchData();
    },
    handleAddAnalysis() {
      this.$refs["add"].show();
    },
    handleEditAnalysis(row) {
      if (row.status !== 10 && row.status !== 60) {
        this.$baseMessage(
          "不允许编辑, 只有未启动或已重置的任务允许编辑",
          "warning"
        );
        return;
      }
      this.$refs["add"].show(row);
    },
    handleShowAnalysis(row) {
      this.$refs["show"].show(row);
    },
    handleDelete(row) {
      if (row.status === 20) {
        this.$baseMessage("当前任务处于运行状态, 不能删除", "warning");
        return;
      }
      this.$baseConfirm("你确定要删除当前项吗", null, async () => {
        const data = await deleteAnalysis(row.id);
        const messages = data.messages;
        this.$baseMessage(messages, "success");
        this.fetchData();
      });
    },
    handleStart(row) {
      if (row.status !== 10 && row.status !== 60) {
        this.$baseMessage(
          "请勿重复启动任务, 如需要启动, 请操作任务为重置状态",
          "warning"
        );
        return;
      }
      this.$baseConfirm("你确定要启动当前项吗", null, async () => {
        const data = await startAnalysis(row.id);
        const messages = data.messages;
        this.$baseMessage(messages, "success");
        this.fetchData();
      });
    },
    handleStop(row) {
      if (row.status !== 20) {
        this.$baseMessage("当前任务未启动, 无法停止", "warning");
        return;
      }
      this.$baseConfirm("你确定要停止当前项吗", null, async () => {
        const data = await stopAnalysis(row.id);
        const messages = data.messages;
        this.$baseMessage(messages, "success");
        this.fetchData();
      });
    },
    handleContinueRun(row) {
      if (row.status !== 30) {
        this.$baseMessage("当前任务未停止, 无法启动继续运行", "warning");
        return;
      }
      this.$baseConfirm("你确定要继续运行当前项吗", null, async () => {
        const data = await continueRunAnalysis(row.id);
        const messages = data.messages;
        this.$baseMessage(messages, "success");
        this.fetchData();
      });
    },
    handleReset(row) {
      if (row.status !== 30 && row.status !== 40 && row.status !== 50) {
        this.$baseMessage(
          "当前任务无法重置, 请先停止任务或等待任务结束",
          "warning"
        );
        return;
      }
      this.$baseConfirm("你确定要重置当前项吗", null, async () => {
        const data = await resetAnalysis(row.id);
        const messages = data.messages;
        this.$baseMessage(messages, "success");
        this.fetchData();
      });
    },
    handlePageSizeChange(val) {
      this.queryForm.page_size = val;
      this.fetchData();
    },
    handleCurrentChange(val) {
      this.queryForm.page = val;
      this.fetchData();
    },
    async fetchData() {
      this.listLoading = true;
      const data = await getAnalysisList(this.queryForm);
      this.listData = data.results;
      this.all_count = data.all_count;
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
    async fetchAnalysisStatus() {
      this.listLoading = true;
      const data = await getAnalysisStatusList();
      this.statusOptions = data.results;
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
    async fetchAnalysisStatistics() {
      this.listLoading = true;
      const data = await getAnalysisStatistics();
      this.statistics = data.results;
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
    /**
     * @return {string}
     */
    StatusTagFilter(val) {
      if (val < 10) {
        return "danger";
      }
      if (val < 20) {
        return "info";
      }
      if (val < 30) {
        return "";
      }
      if (val < 40) {
        return "warning";
      }
      if (val < 50) {
        return "danger";
      }
      if (val < 60) {
        return "success";
      }
      return "danger";
    },
  },
};
</script>

<style scoped></style>
