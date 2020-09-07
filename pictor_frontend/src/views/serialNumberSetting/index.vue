<template>
  <div class="table-container">
    <el-tabs v-model="currentTab" @tab-click="changeTab">
      <el-tab-pane key="project" label="项目编号规则" name="project">
        <vab-query-form>
          <vab-query-form-left-panel>
            <el-button
              icon="el-icon-plus"
              type="primary"
              @click="handleProjectAdd"
              >添加
            </el-button>
          </vab-query-form-left-panel>
          <vab-query-form-right-panel>
            <el-form
              ref="form"
              :model="project_query_form"
              :inline="true"
              @submit.native.prevent
            >
              <el-form-item>
                <el-input
                  v-model="project_query_form.search"
                  placeholder="规则名称"
                />
              </el-form-item>
              <el-form-item>
                <el-button
                  icon="el-icon-search"
                  type="primary"
                  native-type="submit"
                  @click="handleProjectQuery"
                  >查询
                </el-button>
              </el-form-item>
            </el-form>
          </vab-query-form-right-panel>
        </vab-query-form>

        <el-table
          ref="projectNumTable"
          v-loading="listLoading"
          :data="projectList"
          :element-loading-text="elementLoadingText"
          @sort-change="projectTableSortChange"
        >
          <el-table-column
            show-overflow-tooltip
            label="是否启用"
            prop="is_active"
            sortable="custom"
            width="120"
          >
            <template slot-scope="scope">
              <el-tag :type="isActiveStatusFilter(scope.row.is_active)">{{
                isActiveFilter(scope.row.is_active)
              }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column
            show-overflow-tooltip
            label="规则名称"
            prop="name"
            min-width="200"
            sortable="custom"
          >
          </el-table-column>
          <el-table-column
            show-overflow-tooltip
            prop="start_string"
            label="前缀字符"
            width="250"
            sortable="custom"
          ></el-table-column>
          <el-table-column
            show-overflow-tooltip
            label="中间字符生成长度"
            prop="middle_string_len"
            width="200"
            sortable="custom"
          ></el-table-column>
          <el-table-column
            show-overflow-tooltip
            label="后缀字符"
            width="200"
            prop="end_string"
          ></el-table-column>
          <el-table-column
            show-overflow-tooltip
            label="分割字符"
            prop="spilt_string"
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
              <el-button type="text" @click="handleProjectEdit(scope.row)"
                >编辑
              </el-button>
              <el-button type="text" @click="handleProjectDelete(scope.row)"
                >删除
              </el-button>
              <el-button
                v-if="scope.row.is_active"
                type="text"
                @click="handleProjectActivation(scope.row, false)"
                >禁用
              </el-button>
              <el-button
                v-else
                type="text"
                @click="handleProjectActivation(scope.row, true)"
                >启用
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          :background="background"
          :current-page="project_query_form.page"
          :layout="layout"
          :page-size="project_query_form.page_size"
          :total="project_all_count"
          @current-change="handleProjectCurrentChange"
          @size-change="handleProjectSizeChange"
        ></el-pagination>
        <project-num-edit
          ref="project-edit"
          @fetchData="fetchProjectData"
        ></project-num-edit>
      </el-tab-pane>
      <el-tab-pane key="sample" label="样本编号规则" name="sample">
        <vab-query-form>
          <vab-query-form-left-panel>
            <el-button
              icon="el-icon-plus"
              type="primary"
              @click="handleSampleAdd"
              >添加
            </el-button>
          </vab-query-form-left-panel>
          <vab-query-form-right-panel>
            <el-form
              ref="form"
              :model="sample_query_form"
              :inline="true"
              @submit.native.prevent
            >
              <el-form-item>
                <el-input
                  v-model="sample_query_form.search"
                  placeholder="规则名称"
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
          </vab-query-form-right-panel>
        </vab-query-form>

        <el-table
          ref="sampleNumTable"
          v-loading="listLoading"
          :data="sampleList"
          :element-loading-text="elementLoadingText"
          @sort-change="sampleTableSortChange"
        >
          <el-table-column
            show-overflow-tooltip
            label="是否启用"
            prop="is_active"
            sortable="custom"
            width="120"
          >
            <template slot-scope="scope">
              <el-tag :type="isActiveStatusFilter(scope.row.is_active)">{{
                isActiveFilter(scope.row.is_active)
              }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column
            show-overflow-tooltip
            label="规则名称"
            prop="name"
            min-width="200"
            sortable="custom"
          >
          </el-table-column>
          <el-table-column
            show-overflow-tooltip
            prop="start_string"
            label="前缀字符"
            width="250"
            sortable="custom"
          ></el-table-column>
          <el-table-column
            show-overflow-tooltip
            label="中间字符生成长度"
            prop="middle_string_len"
            width="200"
            sortable="custom"
          ></el-table-column>
          <el-table-column
            show-overflow-tooltip
            label="后缀字符"
            width="200"
            prop="end_string"
          ></el-table-column>
          <el-table-column
            show-overflow-tooltip
            label="分割字符"
            prop="spilt_string"
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
              <el-button type="text" @click="handleSampleEdit(scope.row)"
                >编辑
              </el-button>
              <el-button type="text" @click="handleSampleDelete(scope.row)"
                >删除
              </el-button>
              <el-button
                v-if="scope.row.is_active"
                type="text"
                @click="handleSampleActivation(scope.row, false)"
                >禁用
              </el-button>
              <el-button
                v-else
                type="text"
                @click="handleSampleActivation(scope.row, true)"
                >启用
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
        <sample-num-edit
          ref="sample-edit"
          @fetchData="fetchSampleData"
        ></sample-num-edit>
      </el-tab-pane>
      <el-tab-pane key="analysis" label="分析任务编号规则" name="analysis">
        <vab-query-form>
          <vab-query-form-left-panel>
            <el-button
              icon="el-icon-plus"
              type="primary"
              @click="handleAnalysisAdd"
              >添加
            </el-button>
          </vab-query-form-left-panel>
          <vab-query-form-right-panel>
            <el-form
              ref="form"
              :model="analysis_query_form"
              :inline="true"
              @submit.native.prevent
            >
              <el-form-item>
                <el-input
                  v-model="analysis_query_form.search"
                  placeholder="规则名称"
                />
              </el-form-item>
              <el-form-item>
                <el-button
                  icon="el-icon-search"
                  type="primary"
                  native-type="submit"
                  @click="handleAnalysisQuery"
                  >查询
                </el-button>
              </el-form-item>
            </el-form>
          </vab-query-form-right-panel>
        </vab-query-form>

        <el-table
          ref="analysisNumTable"
          v-loading="listLoading"
          :data="analysisList"
          :element-loading-text="elementLoadingText"
          @sort-change="analysisTableSortChange"
        >
          <el-table-column
            show-overflow-tooltip
            label="是否启用"
            prop="is_active"
            sortable="custom"
            width="120"
          >
            <template slot-scope="scope">
              <el-tag :type="isActiveStatusFilter(scope.row.is_active)">{{
                isActiveFilter(scope.row.is_active)
              }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column
            show-overflow-tooltip
            label="规则名称"
            prop="name"
            min-width="200"
            sortable="custom"
          >
          </el-table-column>
          <el-table-column
            show-overflow-tooltip
            prop="start_string"
            label="前缀字符"
            width="250"
            sortable="custom"
          ></el-table-column>
          <el-table-column
            show-overflow-tooltip
            label="中间字符生成长度"
            prop="middle_string_len"
            width="200"
            sortable="custom"
          ></el-table-column>
          <el-table-column
            show-overflow-tooltip
            label="后缀字符"
            width="200"
            prop="end_string"
          ></el-table-column>
          <el-table-column
            show-overflow-tooltip
            label="分割字符"
            prop="spilt_string"
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
              <el-button type="text" @click="handleAnalysisEdit(scope.row)"
                >编辑
              </el-button>
              <el-button type="text" @click="handleAnalysisDelete(scope.row)"
                >删除
              </el-button>
              <el-button
                v-if="scope.row.is_active"
                type="text"
                @click="handleAnalysisActivation(scope.row, false)"
                >禁用
              </el-button>
              <el-button
                v-else
                type="text"
                @click="handleAnalysisActivation(scope.row, true)"
                >启用
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          :background="background"
          :current-page="analysis_query_form.page"
          :layout="layout"
          :page-size="analysis_query_form.page_size"
          :total="analysis_all_count"
          @current-change="handleAnalysisCurrentChange"
          @size-change="handleAnalysisSizeChange"
        ></el-pagination>
        <analysis-num-edit
          ref="analysis-edit"
          @fetchData="fetchAnalysisData"
        ></analysis-num-edit>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import ProjectNumEdit from "./components/ProjectNumEdit";
import SampleNumEdit from "./components/SampleNumEdit";
import AnalysisNumEdit from "./components/AnalysisNumEdit";
import {
  getProjectSerialNumberSettingList,
  deleteProjectSerialNumberSetting,
  bulkDeleteProjectSerialNumberSetting,
  activationProjectSerialNumberSetting,
  getSampleSerialNumberSettingList,
  deleteSampleSerialNumberSetting,
  bulkDeleteSampleSerialNumberSetting,
  activationSampleSerialNumberSetting,
  getAnalysisSerialNumberSettingList,
  deleteAnalysisSerialNumberSetting,
  bulkDeleteAnalysisSerialNumberSetting,
  activationAnalysisSerialNumberSetting,
  getSequencingSerialNumberSettingList,
  deleteSequencingSerialNumberSetting,
  bulkDeleteSequencingSerialNumberSetting,
  activationSequencingSerialNumberSetting,
} from "@/api/serialNumberSetting";
export default {
  name: "ProjectTable",
  components: {
    ProjectNumEdit,
    SampleNumEdit,
    AnalysisNumEdit,
  },
  data() {
    return {
      currentTab: "project",
      listLoading: true,
      background: true,
      layout: "total, sizes, prev, pager, next, jumper",
      elementLoadingText: "正在加载...",
      projectList: [],
      project_all_count: 0,
      project_select_rows: "",
      project_query_form: {
        page: 1,
        page_size: 10,
        search: "",
        ordering: null,
      },
      sampleList: [],
      sample_all_count: 0,
      sample_select_rows: "",
      sample_query_form: {
        page: 1,
        page_size: 10,
        search: "",
        ordering: null,
      },
      analysisList: [],
      analysis_all_count: 0,
      analysis_select_rows: "",
      analysis_query_form: {
        page: 1,
        page_size: 10,
        search: "",
        ordering: null,
      },
      sequencingList: [],
      sequencing_all_count: 0,
      sequencing_select_rows: "",
      sequencing_query_form: {
        page: 1,
        page_size: 10,
        search: "",
        ordering: null,
      },
    };
  },
  created() {
    this.fetchProjectData();
  },
  beforeDestroy() {},
  mounted() {},
  methods: {
    isActiveFilter(is_active) {
      if (is_active === true) {
        return "是";
      } else {
        return "否";
      }
    },
    isActiveStatusFilter(is_active) {
      if (is_active === true) {
        return "success";
      } else {
        return "danger";
      }
    },
    projectTableSortChange(data) {
      const { prop, order } = data;
      if (order === "ascending" || order === null) {
        this.project_query_form.ordering = prop;
      } else {
        this.project_query_form.ordering = `-${prop}`;
      }
      this.fetchProjectData();
    },
    projectSetSelectRows(val) {
      this.project_select_rows = val;
    },
    handleProjectAdd() {
      this.$refs["project-edit"].showEdit();
    },
    handleProjectEdit(row) {
      this.$refs["project-edit"].showEdit(row);
    },
    handleProjectDelete(row) {
      if (row.id) {
        this.$baseConfirm("你确定要删除当前项吗", null, async () => {
          const data = await deleteProjectSerialNumberSetting(row.id);
          const messages = data.messages;
          this.$baseMessage(messages, "success");
          this.fetchProjectData();
        });
      } else {
        if (this.analysis_select_rows.length > 0) {
          const ids = this.analysis_select_rows.map((item) => item.id);
          this.$baseConfirm("你确定要删除选中项吗", null, async () => {
            const data = await bulkDeleteProjectSerialNumberSetting({
              deleted_objects: ids,
            });
            const messages = data.messages;
            this.$baseMessage(messages, "success");
            this.fetchProjectData();
          });
        } else {
          this.$baseMessage("未选中任何行", "error");
          return false;
        }
      }
    },
    handleProjectActivation(row, active = true) {
      let msg = "启用";
      if (!active) {
        msg = "禁用";
      }
      this.$baseConfirm(`你确定要${msg}前项吗`, null, async () => {
        const data = await activationProjectSerialNumberSetting(row.id, {
          active: active,
        });
        const messages = data.messages;
        this.$baseMessage(messages, "success");
        this.fetchProjectData();
      });
    },
    handleProjectSizeChange(val) {
      this.project_query_form.page_size = val;
      this.fetchProjectData();
    },
    handleProjectCurrentChange(val) {
      this.project_query_form.page = val;
      this.fetchProjectData();
    },
    handleProjectQuery() {
      this.project_query_form.page = 1;
      this.fetchProjectData();
    },
    async fetchProjectData() {
      this.listLoading = true;
      const data = await getProjectSerialNumberSettingList(
        this.project_query_form
      );
      this.projectList = data.results;
      this.project_all_count = data.all_count;
      setTimeout(() => {
        this.listLoading = false;
      }, 500);
    },
    ///////////////////////
    sampleTableSortChange(data) {
      const { prop, order } = data;
      if (order === "ascending" || order === null) {
        this.sample_query_form.ordering = prop;
      } else {
        this.sample_query_form.ordering = `-${prop}`;
      }
      this.fetchSampleData();
    },
    sampleSetSelectRows(val) {
      this.sample_select_rows = val;
    },
    handleSampleAdd() {
      this.$refs["sample-edit"].showEdit();
    },
    handleSampleEdit(row) {
      this.$refs["sample-edit"].showEdit(row);
    },
    handleSampleDelete(row) {
      if (row.id) {
        this.$baseConfirm("你确定要删除当前项吗", null, async () => {
          const data = await deleteSampleSerialNumberSetting(row.id);
          const messages = data.messages;
          this.$baseMessage(messages, "success");
          this.fetchSampleData();
        });
      } else {
        if (this.analysis_select_rows.length > 0) {
          const ids = this.analysis_select_rows.map((item) => item.id);
          this.$baseConfirm("你确定要删除选中项吗", null, async () => {
            const data = await bulkDeleteSampleSerialNumberSetting({
              deleted_objects: ids,
            });
            const messages = data.messages;
            this.$baseMessage(messages, "success");
            this.fetchSampleData();
          });
        } else {
          this.$baseMessage("未选中任何行", "error");
          return false;
        }
      }
    },
    handleSampleActivation(row, active = true) {
      let msg = "启用";
      if (!active) {
        msg = "禁用";
      }
      this.$baseConfirm(`你确定要${msg}前项吗`, null, async () => {
        const data = await activationSampleSerialNumberSetting(row.id, {
          active: active,
        });
        const messages = data.messages;
        this.$baseMessage(messages, "success");
        this.fetchSampleData();
      });
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
      const data = await getSampleSerialNumberSettingList(
        this.sample_query_form
      );
      this.sampleList = data.results;
      this.sample_all_count = data.all_count;
      setTimeout(() => {
        this.listLoading = false;
      }, 500);
    },
    ///////////////////////
    analysisTableSortChange(data) {
      const { prop, order } = data;
      if (order === "ascending" || order === null) {
        this.analysis_query_form.ordering = prop;
      } else {
        this.analysis_query_form.ordering = `-${prop}`;
      }
      this.fetchAnalysisData();
    },
    analysisSetSelectRows(val) {
      this.analysis_select_rows = val;
    },
    handleAnalysisAdd() {
      this.$refs["analysis-edit"].showEdit();
    },
    handleAnalysisEdit(row) {
      this.$refs["analysis-edit"].showEdit(row);
    },
    handleAnalysisDelete(row) {
      if (row.id) {
        this.$baseConfirm("你确定要删除当前项吗", null, async () => {
          const data = await deleteAnalysisSerialNumberSetting(row.id);
          const messages = data.messages;
          this.$baseMessage(messages, "success");
          this.fetchAnalysisData();
        });
      } else {
        if (this.analysis_select_rows.length > 0) {
          const ids = this.analysis_select_rows.map((item) => item.id);
          this.$baseConfirm("你确定要删除选中项吗", null, async () => {
            const data = await bulkDeleteAnalysisSerialNumberSetting({
              deleted_objects: ids,
            });
            const messages = data.messages;
            this.$baseMessage(messages, "success");
            this.fetchAnalysisData();
          });
        } else {
          this.$baseMessage("未选中任何行", "error");
          return false;
        }
      }
    },
    handleAnalysisActivation(row, active = true) {
      let msg = "启用";
      if (!active) {
        msg = "禁用";
      }
      this.$baseConfirm(`你确定要${msg}前项吗`, null, async () => {
        const data = await activationAnalysisSerialNumberSetting(row.id, {
          active: active,
        });
        const messages = data.messages;
        this.$baseMessage(messages, "success");
        this.fetchAnalysisData();
      });
    },
    handleAnalysisSizeChange(val) {
      this.analysis_query_form.page_size = val;
      this.fetchAnalysisData();
    },
    handleAnalysisCurrentChange(val) {
      this.analysis_query_form.page = val;
      this.fetchAnalysisData();
    },
    handleAnalysisQuery() {
      this.analysis_query_form.page = 1;
      this.fetchAnalysisData();
    },
    async fetchAnalysisData() {
      this.listLoading = true;
      const data = await getAnalysisSerialNumberSettingList(
        this.analysis_query_form
      );
      this.analysisList = data.results;
      this.analysis_all_count = data.all_count;
      setTimeout(() => {
        this.listLoading = false;
      }, 500);
    },
    ///////////////////////
    sequencingTableSortChange(data) {
      const { prop, order } = data;
      if (order === "ascending" || order === null) {
        this.analysis_query_form.ordering = prop;
      } else {
        this.analysis_query_form.ordering = `-${prop}`;
      }
      this.fetchSequencingData();
    },
    sequencingSetSelectRows(val) {
      this.sequencing_select_rows = val;
    },
    handleSequencingAdd() {
      this.$refs["sequencing-edit"].showEdit();
    },
    handleSequencingEdit(row) {
      this.$refs["sequencing-edit"].showEdit(row);
    },
    handleSequencingDelete(row) {
      if (row.id) {
        this.$baseConfirm("你确定要删除当前项吗", null, async () => {
          const data = await deleteSequencingSerialNumberSetting(row.id);
          const messages = data.messages;
          this.$baseMessage(messages, "success");
          this.fetchSequencingData();
        });
      } else {
        if (this.sequencing_select_rows.length > 0) {
          const ids = this.sequencing_select_rows.map((item) => item.id);
          this.$baseConfirm("你确定要删除选中项吗", null, async () => {
            const data = await bulkDeleteSequencingSerialNumberSetting({
              deleted_objects: ids,
            });
            const messages = data.messages;
            this.$baseMessage(messages, "success");
            this.fetchSequencingData();
          });
        } else {
          this.$baseMessage("未选中任何行", "error");
          return false;
        }
      }
    },
    handleSequencingActivation(row, active = true) {
      let msg = "启用";
      if (!active) {
        msg = "禁用";
      }
      this.$baseConfirm(`你确定要${msg}前项吗`, null, async () => {
        const data = await activationSequencingSerialNumberSetting(row.id, {
          active: active,
        });
        const messages = data.messages;
        this.$baseMessage(messages, "success");
        this.fetchSequencingData();
      });
    },
    handleSequencingSizeChange(val) {
      this.sequencing_query_form.page_size = val;
      this.fetchSequencingData();
    },
    handleSequencingCurrentChange(val) {
      this.sequencing_query_form.page = val;
      this.fetchSequencingData();
    },
    handleSequencingQuery() {
      this.sequencing_query_form.page = 1;
      this.fetchSequencingData();
    },
    async fetchSequencingData() {
      this.listLoading = true;
      const data = await getSequencingSerialNumberSettingList(
        this.sequencing_query_form
      );
      this.sequencingList = data.results;
      this.sequencing_all_count = data.all_count;
      setTimeout(() => {
        this.listLoading = false;
      }, 500);
    },
    changeTab(obj, e) {
      console.log("changeTab", obj.$vnode.key);
      if (obj.$vnode.key === "project") {
        this.fetchProjectData();
      }
      if (obj.$vnode.key === "sample") {
        this.fetchSampleData();
      }
      if (obj.$vnode.key === "analysis") {
        this.fetchAnalysisData();
      }
      if (obj.$vnode.key === "sequencing") {
        this.fetchSequencingData();
      }
    },
  },
};
</script>
