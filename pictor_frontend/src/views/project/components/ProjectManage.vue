<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogTableVisible"
    width="80%"
    @close="close"
  >
    <div class="table-container">
      <div id="info">
        <el-divider content-position="center">
          <i class="el-icon-mobile-phone"></i
          ><el-tag type="primary">基础信息</el-tag>
        </el-divider>
        <div class="elp-desc-list center_div">
          <div class="elp-desc-list-row">
            <div class="row-item">
              <h4>项目编号：</h4>
              <span>{{ project.serial_number }}</span>
            </div>
            <div class="row-item">
              <h4>项目名称：</h4>
              <span>{{ project.name }}</span>
            </div>
            <div class="row-item">
              <h4>创建时间：</h4>
              <span>{{ project.created_time }}</span>
            </div>
          </div>
          <div class="elp-desc-list-row">
            <div class="row-item">
              <h4>备注/描述：</h4>
              <span>{{ project.remark }}</span>
            </div>
          </div>
        </div>
      </div>
      <el-divider content-position="center">
        <i class="el-icon-mobile-phone"></i
        ><el-tag type="primary">样本/分析任务数目</el-tag>
      </el-divider>
      <el-card class="dk-box-card-main" shadow="never">
        <dk-list-key-value
          class="dk-normal-list-header"
          :xs="24"
          :sm="8"
          :list="sample_statistics"
        ></dk-list-key-value>
      </el-card>
      <el-divider content-position="center"> </el-divider>
      <el-card class="dk-box-card-main" shadow="never">
        <dk-list-key-value
          class="dk-normal-list-header"
          :xs="24"
          :sm="8"
          :list="analysis_statistics"
        ></dk-list-key-value>
      </el-card>
      <el-divider content-position="center">
        <i class="el-icon-mobile-phone"></i
        ><el-tag type="primary">关联数据</el-tag>
      </el-divider>
      <el-tabs v-model="currentTab" @tab-click="changeTab">
        <el-tab-pane key="sample" label="样本" name="sample">
          <vab-query-form>
            <vab-query-form-left-panel>
              <el-form
                ref="form"
                :model="sample_query_form"
                :inline="true"
                @submit.native.prevent
              >
                <el-form-item>
                  <el-input
                    v-model="sample_query_form.search"
                    placeholder="样本编号"
                  />
                </el-form-item>
                <el-form-item>
                  <el-button
                    icon="el-icon-search"
                    type="primary"
                    native-type="submit"
                    @click="handleSampleQuery"
                    >查询
                  </el-button>
                </el-form-item>
              </el-form>
            </vab-query-form-left-panel>
          </vab-query-form>

          <el-table
            ref="sampleTable"
            v-loading="listLoading"
            :data="sample_list"
            :element-loading-text="elementLoadingText"
            @sort-change="tableSampleSortChange"
          >
            <el-table-column
              show-overflow-tooltip
              label="所属项目"
              prop="project.name"
              sortable="custom"
            >
              <template v-if="scope.row.project" slot-scope="scope">
                <el-popover trigger="hover" placement="top">
                  <p>项目编号: {{ scope.row.project.serial_number }}</p>
                  <p>项目名称: {{ scope.row.project.name }}</p>
                  <div slot="reference" class="name-wrapper">
                    <el-tag size="medium">{{ scope.row.project.name }}</el-tag>
                  </div>
                </el-popover>
              </template>
            </el-table-column>
            <el-table-column
              show-overflow-tooltip
              label="样本编号"
              prop="serial_number"
              sortable="custom"
            >
            </el-table-column>
            <el-table-column
              show-overflow-tooltip
              prop="sample_name"
              label="样本名称"
              sortable="custom"
            >
            </el-table-column>
            <el-table-column
              show-overflow-tooltip
              prop="sample_type"
              label="样本类型"
              sortable="custom"
            >
            </el-table-column>
            <el-table-column
              show-overflow-tooltip
              prop="related_files_count"
              label="关键文件数"
              sortable="custom"
            >
              <template slot-scope="scope">
                <el-tag
                  v-if="scope.row.dataset_count"
                  size="medium"
                  type="success"
                  >{{ scope.row.dataset_count }}</el-tag
                >
                <el-tag v-else size="medium" type="danger">{{
                  scope.row.dataset_count
                }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              show-overflow-tooltip
              prop="sample_source"
              label="样本来源"
              sortable="custom"
            >
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
                <el-button
                  v-if="sample_permissions.edit"
                  type="text"
                  @click="handleSampleEdit(scope.row)"
                  >编辑
                </el-button>
                <el-button
                  v-if="sample_permissions.related"
                  type="text"
                  @click="handleSampleSelectData(scope.row)"
                  >关联数据
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            :background="background"
            :current-page="sample_query_form.page"
            :layout="layout"
            :page-size="sample_query_form.page_size"
            :total="sample_all_count"
            @current-change="handleSampleCurrentChange"
            @size-change="handleSampleSizeChange"
          ></el-pagination>
          <sample-edit ref="edit" @fetchData="fetchSampleData"></sample-edit>
          <select-dataset
            ref="dataset"
            @fetchData="fetchSampleData"
          ></select-dataset>
        </el-tab-pane>
        <el-tab-pane key="analysis" label="分析" name="analysis">
          <el-card class="dk-box-card-main" shadow="never">
            <!-- 搜索表单 -->
            <el-form
              action="javascript:void(0);"
              :inline="true"
              :model="analysis_query_form"
              size="small"
              class="dk-search-form"
              @submit.native="submitAnalysisSearchForm"
            >
              <el-form-item key="status" prop="status">
                <el-radio-group
                  v-model="analysis_query_form.status"
                  @change="submitAnalysisSelectStatus"
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
                <el-input
                  v-model="analysis_query_form.search"
                  placeholder="请输入分析编号"
                >
                  <el-button
                    slot="append"
                    icon="el-icon-search"
                    native-type="submit"
                  ></el-button>
                </el-input>
              </el-form-item>
            </el-form>
            <el-table
              class="dk-normal-list"
              :data="analysis_list"
              :show-header="true"
            >
              <el-table-column min-width="250">
                <template slot-scope="scope">
                  <dk-list :is-single-data="true" :list="scope.row"></dk-list>
                </template>
              </el-table-column>
              <el-table-column width="150">
                <template slot-scope="scope">
                  <span class="dk-normal-list-header">项目</span>
                  <p>
                    {{ scope.row.project.serial_number }}({{
                      scope.row.project.name
                    }})
                  </p>
                </template>
              </el-table-column>
              <el-table-column width="150">
                <template slot-scope="scope">
                  <span class="dk-normal-list-header">模块</span>
                  <p>
                    {{ scope.row.analysis_module.name }}
                  </p>
                </template>
              </el-table-column>
              <el-table-column width="150">
                <template slot-scope="scope">
                  <span class="dk-normal-list-header">模块版本</span>
                  <p>
                    {{ scope.row.analysis_module.version }}
                  </p>
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
                      <el-dropdown-item
                        v-if="analysis_permissions.edit"
                        @click.native="handleEditAnalysis(scope.row)"
                        >编辑</el-dropdown-item
                      >
                      <el-dropdown-item
                        v-if="analysis_permissions.delete"
                        @click.native="handleDelete(scope.row)"
                        >删除</el-dropdown-item
                      >
                      <el-dropdown-item
                        v-if="analysis_permissions.start"
                        @click.native="handleStart(scope.row)"
                        >启动</el-dropdown-item
                      >
                      <el-dropdown-item
                        v-if="analysis_permissions.stop"
                        @click.native="handleStop(scope.row)"
                        >停止</el-dropdown-item
                      >
                      <el-dropdown-item
                        v-if="analysis_permissions.continue"
                        @click.native="handleContinueRun(scope.row)"
                        >继续运行</el-dropdown-item
                      >
                      <el-dropdown-item
                        v-if="analysis_permissions.reset"
                        @click.native="handleReset(scope.row)"
                        >重置</el-dropdown-item
                      >
                    </el-dropdown-menu>
                  </el-dropdown>
                </template>
              </el-table-column>
            </el-table>
            <!-- 分页 -->
            <el-pagination
              class="dk-pagination"
              background
              :current-page="analysis_query_form.page"
              :page-sizes="[10, 50, 100, 200, 300, 400]"
              :page-size="analysis_query_form.page_size"
              :layout="layout"
              :pager-count="5"
              :total="analysis_all_count"
              @size-change="handleAnalysisPageSizeChange"
              @current-change="handleAnalysisCurrentChange"
            >
            </el-pagination>
          </el-card>
          <add-analysis ref="add" @fetchData="fetchAnalysisData"></add-analysis>
          <show-analysis
            ref="show"
            @fetchData="fetchAnalysisData"
          ></show-analysis>
        </el-tab-pane>
        <el-tab-pane key="project_dataset" label="数据" name="project_dataset">
          <dataset
            ref="project_dataset"
            :data-header-visible="dataset_param.dataHeaderVisible"
            :data-search-visible="dataset_param.dataSearchVisible"
            :data-explorer-visible="dataset_param.dataExplorerVisible"
            :show-list="dataset_param.showList"
            :only-directory="dataset_param.onlyDirectory"
            :only-file="dataset_param.onlyFile"
            :only-show-current="dataset_param.onlyShowCurrent"
            :show-border="dataset_param.showBorder"
            :show-checkbox="dataset_param.showCheckbox"
            :show-index="dataset_param.showIndex"
            :click-file-type="dataset_param.clickFileType"
            :checked-file-call-back="dataset_param.checkedFileCallBack"
            :only-show-one-list="dataset_param.onlyShowOneList"
            :data-type="dataset_param.dataType"
            :current-path="dataset_param.currentPath"
          ></dataset>
        </el-tab-pane>
      </el-tabs>
    </div>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">关 闭</el-button>
    </div>
  </el-dialog>
</template>

<script>
import DkListKeyValue from "@/components/DKComponents/list/DkListKeyValue"; // 导入
import DkList from "@/components/DKComponents/list/DkList"; // 导入
import Dataset from "@/components/DataSet"; // 导入文件管理器
import {
  getProjectStatistics,
  updateProject,
  retrieveProject,
} from "@/api/project";
import SampleEdit from "../../sample/components/SampleEdit";
import SelectDataset from "../../sample/components/SelectDataset";
import { getSampleList, deleteSample, bulkDeleteSample } from "@/api/sample";
import ShowAnalysis from "../../analysis/components/ShowAnalysis";
import AddAnalysis from "../../analysis/components/AddAnalysis";
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
import { getActionPermission } from "@/api/actionPermission";

export default {
  name: "ProjectManage",
  components: {
    SampleEdit,
    SelectDataset,
    AddAnalysis,
    ShowAnalysis,
    DkList,
    DkListKeyValue,
    Dataset,
  },
  data() {
    return {
      title: "",
      currentTab: "sample",
      dialogTableVisible: false,
      listLoading: true,
      layout: "total, sizes, prev, pager, next, jumper",
      background: true,
      elementLoadingText: "正在加载...",
      project: {},
      sample_list: [],
      sample_all_count: 0,
      sample_query_form: {
        page: 1,
        project: 1,
        page_size: 10,
        search: "",
        ordering: null,
      },
      sample_statistics: [
        { key: "样本数", value: "0" },
        { key: "已关联数据样本数", value: "0" },
        { key: "本月新增样本数", value: "0" },
      ],
      analysis_statistics: [
        { key: "总任务数", value: "0" },
        { key: "本月任务平均处理时间", value: "0" },
        { key: "本月完成任务数", value: "0" },
      ],
      analysis_list: [],
      analysis_query_form: {
        search: "",
        status: null,
        page: 1,
        project: 1,
        page_size: 10,
        ordering: null,
      },
      analysis_all_count: 0,
      statusOptions: {},
      dataset_param: {
        dataHeaderVisible: false, // 是否显示头部操作栏
        dataSearchVisible: true, // 是否显示搜索框
        dataExplorerVisible: true, // 是否显示搜索框
        showList: false, // 是否以表格形式展示
        onlyDirectory: false, // 是否仅仅展示文件夹
        onlyFile: false, // 是否仅仅展示文件
        onlyShowCurrent: false, // 是否仅展示当前类型的数据
        showBorder: true, // 表格是否显示边框
        showCheckbox: true, // 是否显示复选框
        showIndex: true, // 是否显示顺序号
        clickFileType: 1, // 点击文件触发形式, 0为点击文件即下载/1为点击文件为选择
        checkedFileCallBack: true, // 是否返回已选文件
        onlyShowOneList: true,
        dataType: 10,
        currentPath: "",
      },
      sample_permissions: {},
      analysis_permissions: {},
    };
  },
  created() {
    this.fetchPermission();
    this.fetchAnalysisStatus();
  },
  methods: {
    async fetchPermission() {
      const data = await getActionPermission({ permission_type: "sample" });
      const analysis_data = await getActionPermission({
        permission_type: "analysis",
      });
      this.sample_permissions = data.results.sample;
      this.analysis_permissions = analysis_data.results.analysis;
    },
    showMange(row) {
      this.project = row;
      this.sample_query_form.project = row.id;
      this.analysis_query_form.project = row.id;
      this.title = `${row.serial_number}(${row.name})`;
      if (this.currentTab === "sample") {
        this.fetchSampleData();
      }
      this.fetchProjectStatistics(row);
      this.dialogTableVisible = true;
    },
    close() {
      this.currentTab = "sample";
      this.title = "";
      this.project = {};
      this.dialogTableVisible = false;
    },
    changeTab(obj, e) {
      console.log("changeTab", obj.$vnode.key);
      if (obj.$vnode.key === "sample") {
        console.log("changeTab", obj.$vnode.key);
        this.fetchSampleData();
      }
      if (obj.$vnode.key === "analysis") {
        console.log("changeTab", obj.$vnode.key);
        this.fetchAnalysisData();
      }
      if (obj.$vnode.key === "project_dataset") {
        console.log("changeTab", obj.$vnode.key);
        this.dataset_param.dataType = 30; // 项目数据
        this.dataset_param.currentPath = this.project.serial_number;
        this.$refs["project_dataset"].setDataCurrentPath(
          this.dataset_param.currentPath
        );
        this.$refs["project_dataset"].setDataCurrentType(
          this.dataset_param.dataType
        );
        this.$refs["project_dataset"].getFileList(this.dataset_param.dataType);
      }
    },
    handleSampleSelectData(row) {
      this.$refs["dataset"].showSelectData(row);
    },
    tableSampleSortChange(data) {
      const { prop, order } = data;
      if (order === "ascending" || order === null) {
        this.sample_query_form.ordering = prop;
      } else {
        this.sample_query_form.ordering = `-${prop}`;
      }
      this.fetchSampleData();
    },
    handleSampleAdd() {
      this.$refs["edit"].showEdit();
    },
    handleSampleEdit(row) {
      this.$refs["edit"].showEdit(row);
    },
    handleSampleSizeChange(val) {
      this.sample_query_form.page_size = val;
      this.fetchSampleData();
    },
    handleSampleCurrentChange(val) {
      this.sample_query_form.page = val;
      this.fetchSampleData();
    },
    handleSampleQuery() {
      this.sample_query_form.page = 1;
      this.fetchSampleData();
    },
    async fetchSampleData() {
      this.listLoading = true;
      const data = await getSampleList(this.sample_query_form);
      this.sample_list = data.results;
      this.sample_all_count = data.all_count;
      setTimeout(() => {
        this.listLoading = false;
      }, 500);
    },
    ///////////////////////////
    submitAnalysisSearchForm() {
      this.fetchAnalysisData();
    },
    submitAnalysisSelectStatus(val) {
      this.analysis_query_form.status = val;
      this.fetchAnalysisData();
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
        this.fetchAnalysisData();
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
        this.fetchAnalysisData();
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
        this.fetchAnalysisData();
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
        this.fetchAnalysisData();
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
        this.fetchAnalysisData();
      });
    },
    handleAnalysisPageSizeChange(val) {
      this.analysis_query_form.page_size = val;
      this.fetchAnalysisData();
    },
    handleAnalysisCurrentChange(val) {
      this.analysis_query_form.page = val;
      this.fetchAnalysisData();
    },
    async fetchAnalysisData() {
      this.listLoading = true;
      const data = await getAnalysisList(this.analysis_query_form);
      this.analysis_list = data.results;
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
    async fetchProjectStatistics(row) {
      this.listLoading = true;
      const data = await getProjectStatistics(row.id);
      this.sample_statistics = data.results.sample_statistics;
      this.analysis_statistics = data.results.analysis_statistics;
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
<style lang="scss" scoped>
.elp-step-success-icon {
  text-align: center;
  font-size: 60px;
  color: #49bc19;
}
.elp-step-success-info {
  text-align: center;
  line-height: 70px;
}
.elp-step-success-card {
  background: #f9f9f9;
  padding: 20px 80px;
  line-height: 50px;
  text-align: center;
  span {
    color: #666;
  }
}
.elp-button {
  display: flex;
  justify-content: center;
}
.elp-desc-list {
  padding: 10px 10px;
  color: #666;
  font-size: 14px;
  span {
    color: #777;
  }
  .elp-desc-list-head {
    color: #000;
    font-size: 15px;
    line-height: 60px;
  }
  .elp-desc-list-row {
    line-height: 30px;
    display: flex;
    h6 {
      font-size: 14px;
      margin: 0;
    }
    .row-item {
      display: flex;
      width: 100%;
    }
  }
}
</style>
