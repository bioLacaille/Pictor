<template>
  <div class="table-container">
    <vab-query-form>
      <vab-query-form-left-panel>
        <el-button icon="el-icon-plus" type="primary" @click="handleAnalysisAdd"
          >添加
        </el-button>
        <!--        <el-button-->
        <!--          icon="el-icon-delete"-->
        <!--          type="danger"-->
        <!--          @click="handleAnalysisDelete"-->
        <!--          >删除-->
        <!--        </el-button>-->
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
              placeholder="项目编号/项目名称"
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
      ref="analysisInterFaceTable"
      v-loading="listLoading"
      :data="analysisList"
      :element-loading-text="elementLoadingText"
      @sort-change="analysisTableSortChange"
    >
      <!--      <el-table-column-->
      <!--        show-overflow-tooltip-->
      <!--        type="selection"-->
      <!--        width="55"-->
      <!--      ></el-table-column>-->
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
        label="接口名称"
        prop="name"
        width="200"
        sortable="custom"
      >
      </el-table-column>
      <el-table-column
        show-overflow-tooltip
        prop="domain"
        label="接口域名"
        width="250"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="成功返回码"
        prop="success_code"
        width="200"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="失败返回码"
        width="200"
        prop="error_code"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="启动任务URI"
        prop="start_uri"
        width="200"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="停止任务URI"
        prop="stop_uri"
        width="200"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="继续运行任务URI"
        prop="continue_uri"
        width="200"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="重置任务URI"
        prop="reset_uri"
        width="200"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="查询任务状态URI"
        prop="status_uri"
        width="200"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="获取任务结果URI"
        prop="result_uri"
        width="200"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="获取运行日志URI"
        prop="log_uri"
        width="200"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="创建日期"
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
    <task-interface-edit
      ref="analysis-edit"
      @fetchData="fetchAnalysisData"
    ></task-interface-edit>
    <!--    <el-tabs v-model="currentTab" @tab-click="changeTab">-->
    <!--      <el-tab-pane key="analysis" label="分析接口" name="analysis">-->
    <!--        <vab-query-form>-->
    <!--          <vab-query-form-left-panel>-->
    <!--            <el-button-->
    <!--              icon="el-icon-plus"-->
    <!--              type="primary"-->
    <!--              @click="handleAnalysisAdd"-->
    <!--              >添加-->
    <!--            </el-button>-->
    <!--            &lt;!&ndash;        <el-button&ndash;&gt;-->
    <!--            &lt;!&ndash;          icon="el-icon-delete"&ndash;&gt;-->
    <!--            &lt;!&ndash;          type="danger"&ndash;&gt;-->
    <!--            &lt;!&ndash;          @click="handleAnalysisDelete"&ndash;&gt;-->
    <!--            &lt;!&ndash;          >删除&ndash;&gt;-->
    <!--            &lt;!&ndash;        </el-button>&ndash;&gt;-->
    <!--          </vab-query-form-left-panel>-->
    <!--          <vab-query-form-right-panel>-->
    <!--            <el-form-->
    <!--              ref="form"-->
    <!--              :model="analysis_query_form"-->
    <!--              :inline="true"-->
    <!--              @submit.native.prevent-->
    <!--            >-->
    <!--              <el-form-item>-->
    <!--                <el-input-->
    <!--                  v-model="analysis_query_form.search"-->
    <!--                  placeholder="项目编号/项目名称"-->
    <!--                />-->
    <!--              </el-form-item>-->
    <!--              <el-form-item>-->
    <!--                <el-button-->
    <!--                  icon="el-icon-search"-->
    <!--                  type="primary"-->
    <!--                  native-type="submit"-->
    <!--                  @click="handleAnalysisQuery"-->
    <!--                  >查询-->
    <!--                </el-button>-->
    <!--              </el-form-item>-->
    <!--            </el-form>-->
    <!--          </vab-query-form-right-panel>-->
    <!--        </vab-query-form>-->

    <!--        <el-table-->
    <!--          ref="analysisInterFaceTable"-->
    <!--          v-loading="listLoading"-->
    <!--          :data="analysisList"-->
    <!--          :element-loading-text="elementLoadingText"-->
    <!--          @sort-change="analysisTableSortChange"-->
    <!--        >-->
    <!--          &lt;!&ndash;      <el-table-column&ndash;&gt;-->
    <!--          &lt;!&ndash;        show-overflow-tooltip&ndash;&gt;-->
    <!--          &lt;!&ndash;        type="selection"&ndash;&gt;-->
    <!--          &lt;!&ndash;        width="55"&ndash;&gt;-->
    <!--          &lt;!&ndash;      ></el-table-column>&ndash;&gt;-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="是否启用"-->
    <!--            prop="is_active"-->
    <!--            sortable="custom"-->
    <!--            width="120"-->
    <!--          >-->
    <!--            <template slot-scope="scope">-->
    <!--              <el-tag :type="isActiveStatusFilter(scope.row.is_active)">{{-->
    <!--                isActiveFilter(scope.row.is_active)-->
    <!--              }}</el-tag>-->
    <!--            </template>-->
    <!--          </el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="接口名称"-->
    <!--            prop="name"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          >-->
    <!--          </el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            prop="domain"-->
    <!--            label="接口域名"-->
    <!--            width="250"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="成功返回码"-->
    <!--            prop="success_code"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="失败返回码"-->
    <!--            width="200"-->
    <!--            prop="error_code"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="启动任务URI"-->
    <!--            prop="start_uri"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="停止任务URI"-->
    <!--            prop="stop_uri"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="继续运行任务URI"-->
    <!--            prop="continue_uri"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="重置任务URI"-->
    <!--            prop="reset_uri"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="查询任务状态URI"-->
    <!--            prop="status_uri"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="获取任务结果URI"-->
    <!--            prop="result_uri"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="获取运行日志URI"-->
    <!--            prop="log_uri"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="创建日期"-->
    <!--            prop="created_time"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="操作"-->
    <!--            width="180px"-->
    <!--            fixed="right"-->
    <!--          >-->
    <!--            <template slot-scope="scope">-->
    <!--              <el-button type="text" @click="handleAnalysisEdit(scope.row)"-->
    <!--                >编辑-->
    <!--              </el-button>-->
    <!--              <el-button type="text" @click="handleAnalysisDelete(scope.row)"-->
    <!--                >删除-->
    <!--              </el-button>-->
    <!--              <el-button-->
    <!--                v-if="scope.row.is_active"-->
    <!--                type="text"-->
    <!--                @click="handleAnalysisActivation(scope.row, false)"-->
    <!--                >禁用-->
    <!--              </el-button>-->
    <!--              <el-button-->
    <!--                v-else-->
    <!--                type="text"-->
    <!--                @click="handleAnalysisActivation(scope.row, true)"-->
    <!--                >启用-->
    <!--              </el-button>-->
    <!--            </template>-->
    <!--          </el-table-column>-->
    <!--        </el-table>-->
    <!--        <el-pagination-->
    <!--          :background="background"-->
    <!--          :current-page="analysis_query_form.page"-->
    <!--          :layout="layout"-->
    <!--          :page-size="analysis_query_form.page_size"-->
    <!--          :total="analysis_all_count"-->
    <!--          @current-change="handleAnalysisCurrentChange"-->
    <!--          @size-change="handleAnalysisSizeChange"-->
    <!--        ></el-pagination>-->
    <!--        <task-interface-edit-->
    <!--          ref="analysis-edit"-->
    <!--          @fetchData="fetchAnalysisData"-->
    <!--        ></task-interface-edit>-->
    <!--      </el-tab-pane>-->
    <!--      <el-tab-pane key="sequencing" label="拆分接口" name="sequencing">-->
    <!--        <vab-query-form>-->
    <!--          <vab-query-form-left-panel>-->
    <!--            <el-button-->
    <!--              icon="el-icon-plus"-->
    <!--              type="primary"-->
    <!--              @click="handleSequencingAdd"-->
    <!--              >添加-->
    <!--            </el-button>-->
    <!--            &lt;!&ndash;        <el-button&ndash;&gt;-->
    <!--            &lt;!&ndash;          icon="el-icon-delete"&ndash;&gt;-->
    <!--            &lt;!&ndash;          type="danger"&ndash;&gt;-->
    <!--            &lt;!&ndash;          @click="handleAnalysisDelete"&ndash;&gt;-->
    <!--            &lt;!&ndash;          >删除&ndash;&gt;-->
    <!--            &lt;!&ndash;        </el-button>&ndash;&gt;-->
    <!--          </vab-query-form-left-panel>-->
    <!--          <vab-query-form-right-panel>-->
    <!--            <el-form-->
    <!--              ref="form"-->
    <!--              :model="sequencing_query_form"-->
    <!--              :inline="true"-->
    <!--              @submit.native.prevent-->
    <!--            >-->
    <!--              <el-form-item>-->
    <!--                <el-input-->
    <!--                  v-model="sequencing_query_form.search"-->
    <!--                  placeholder="接口名称"-->
    <!--                />-->
    <!--              </el-form-item>-->
    <!--              <el-form-item>-->
    <!--                <el-button-->
    <!--                  icon="el-icon-search"-->
    <!--                  type="primary"-->
    <!--                  native-type="submit"-->
    <!--                  @click="handleSequencingQuery"-->
    <!--                  >查询-->
    <!--                </el-button>-->
    <!--              </el-form-item>-->
    <!--            </el-form>-->
    <!--          </vab-query-form-right-panel>-->
    <!--        </vab-query-form>-->

    <!--        <el-table-->
    <!--          ref="sequencingInterFaceTable"-->
    <!--          v-loading="listLoading"-->
    <!--          :data="sequencingList"-->
    <!--          :element-loading-text="elementLoadingText"-->
    <!--          @sort-change="sequencingTableSortChange"-->
    <!--        >-->
    <!--          &lt;!&ndash;      <el-table-column&ndash;&gt;-->
    <!--          &lt;!&ndash;        show-overflow-tooltip&ndash;&gt;-->
    <!--          &lt;!&ndash;        type="selection"&ndash;&gt;-->
    <!--          &lt;!&ndash;        width="55"&ndash;&gt;-->
    <!--          &lt;!&ndash;      ></el-table-column>&ndash;&gt;-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="是否启用"-->
    <!--            prop="is_active"-->
    <!--            sortable="custom"-->
    <!--            width="120"-->
    <!--          >-->
    <!--            <template slot-scope="scope">-->
    <!--              <el-tag :type="isActiveStatusFilter(scope.row.is_active)">{{-->
    <!--                isActiveFilter(scope.row.is_active)-->
    <!--              }}</el-tag>-->
    <!--            </template>-->
    <!--          </el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="接口名称"-->
    <!--            prop="name"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          >-->
    <!--          </el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            prop="domain"-->
    <!--            label="接口域名"-->
    <!--            width="250"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="成功返回码"-->
    <!--            prop="success_code"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="失败返回码"-->
    <!--            width="200"-->
    <!--            prop="error_code"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="启动任务URI"-->
    <!--            prop="start_uri"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="停止任务URI"-->
    <!--            prop="stop_uri"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="重置任务URI"-->
    <!--            prop="reset_uri"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="查询任务状态URI"-->
    <!--            prop="status_uri"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="获取任务结果URI"-->
    <!--            prop="result_uri"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="获取运行日志URI"-->
    <!--            prop="log_uri"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="创建日期"-->
    <!--            prop="created_time"-->
    <!--            width="200"-->
    <!--            sortable="custom"-->
    <!--          ></el-table-column>-->
    <!--          <el-table-column-->
    <!--            show-overflow-tooltip-->
    <!--            label="操作"-->
    <!--            width="180px"-->
    <!--            fixed="right"-->
    <!--          >-->
    <!--            <template slot-scope="seq_scope">-->
    <!--              <el-button-->
    <!--                type="text"-->
    <!--                @click="handleSequencingEdit(seq_scope.row)"-->
    <!--                >编辑-->
    <!--              </el-button>-->
    <!--              <el-button-->
    <!--                type="text"-->
    <!--                @click="handleSequencingDelete(seq_scope.row)"-->
    <!--                >删除-->
    <!--              </el-button>-->
    <!--              <el-button-->
    <!--                v-if="seq_scope.row.is_active"-->
    <!--                type="text"-->
    <!--                @click="handleSequencingActivation(seq_scope.row, false)"-->
    <!--                >禁用-->
    <!--              </el-button>-->
    <!--              <el-button-->
    <!--                v-else-->
    <!--                type="text"-->
    <!--                @click="handleSequencingActivation(seq_scope.row, true)"-->
    <!--                >启用-->
    <!--              </el-button>-->
    <!--            </template>-->
    <!--          </el-table-column>-->
    <!--        </el-table>-->
    <!--        <el-pagination-->
    <!--          :background="background"-->
    <!--          :current-page="sequencing_query_form.page"-->
    <!--          :layout="layout"-->
    <!--          :page-size="sequencing_query_form.page_size"-->
    <!--          :total="sequencing_all_count"-->
    <!--          @current-change="handleSequencingCurrentChange"-->
    <!--          @size-change="handleSequencingSizeChange"-->
    <!--        ></el-pagination>-->
    <!--        <seq-task-interface-edit-->
    <!--          ref="sequencing-edit"-->
    <!--          @fetchData="fetchSequencingData"-->
    <!--        ></seq-task-interface-edit>-->
    <!--      </el-tab-pane>-->
    <!--    </el-tabs>-->
  </div>
</template>

<script>
import TaskInterfaceEdit from "./components/TaskInterfaceEdit";
import SeqTaskInterfaceEdit from "./components/SeqTaskInterfaceEdit";
import {
  getAnalysisTaskInterfaceList,
  deleteAnalysisTaskInterface,
  bulkDeleteAnalysisTaskInterface,
  activationAnalysisTaskInterface,
  getSequencingTaskInterfaceList,
  deleteSequencingTaskInterface,
  bulkDeleteSequencingTaskInterface,
  activationSequencingTaskInterface,
} from "@/api/task_interface";
export default {
  name: "ProjectTable",
  components: {
    TaskInterfaceEdit,
    // SeqTaskInterfaceEdit,
  },
  data() {
    return {
      currentTab: "analysis",
      listLoading: true,
      background: true,
      layout: "total, sizes, prev, pager, next, jumper",
      elementLoadingText: "正在加载...",
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
    this.fetchAnalysisData();
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
    analysisTableSortChange(data) {
      const { prop, order } = data;
      if (order === "ascending" || order === null) {
        this.analysis_query_form.ordering = prop;
      } else {
        this.analysis_query_form.ordering = `-${prop}`;
      }
      this.fetchAnalysisData();
    },
    sequencingTableSortChange(data) {
      const { prop, order } = data;
      if (order === "ascending" || order === null) {
        this.sequencing_query_form.ordering = prop;
      } else {
        this.sequencing_query_form.ordering = `-${prop}`;
      }
      this.fetchAnalysisData();
    },
    analysisSetSelectRows(val) {
      this.analysis_select_rows = val;
    },
    sequencingSetSelectRows(val) {
      this.sequencing_select_rows = val;
    },
    handleAnalysisAdd() {
      this.$refs["analysis-edit"].showEdit();
    },
    handleSequencingAdd() {
      this.$refs["sequencing-edit"].showEdit();
    },
    handleAnalysisEdit(row) {
      this.$refs["analysis-edit"].showEdit(row);
    },
    handleSequencingEdit(row) {
      this.$refs["sequencing-edit"].showEdit(row);
    },
    handleAnalysisDelete(row) {
      if (row.id) {
        this.$baseConfirm("你确定要删除当前项吗", null, async () => {
          const data = await deleteAnalysisTaskInterface(row.id);
          const messages = data.messages;
          this.$baseMessage(messages, "success");
          this.fetchAnalysisData();
        });
      } else {
        if (this.analysis_select_rows.length > 0) {
          const ids = this.analysis_select_rows.map((item) => item.id);
          this.$baseConfirm("你确定要删除选中项吗", null, async () => {
            const data = await bulkDeleteAnalysisTaskInterface({
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
    handleSequencingDelete(row) {
      if (row.id) {
        this.$baseConfirm("你确定要删除当前项吗", null, async () => {
          const data = await deleteSequencingTaskInterface(row.id);
          const messages = data.messages;
          this.$baseMessage(messages, "success");
          this.fetchSequencingData();
        });
      } else {
        if (this.sequencing_select_rows.length > 0) {
          const ids = this.sequencing_select_rows.map((item) => item.id);
          this.$baseConfirm("你确定要删除选中项吗", null, async () => {
            const data = await bulkDeleteSequencingTaskInterface({
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
    handleAnalysisActivation(row, active = true) {
      let msg = "启用";
      if (!active) {
        msg = "禁用";
      }
      this.$baseConfirm(`你确定要${msg}前项吗`, null, async () => {
        const data = await activationAnalysisTaskInterface(row.id, {
          active: active,
        });
        const messages = data.messages;
        this.$baseMessage(messages, "success");
        this.fetchAnalysisData();
      });
    },
    handleSequencingActivation(row, active = true) {
      let msg = "启用";
      if (!active) {
        msg = "禁用";
      }
      this.$baseConfirm(`你确定要${msg}前项吗`, null, async () => {
        const data = await activationSequencingTaskInterface(row.id, {
          active: active,
        });
        const messages = data.messages;
        this.$baseMessage(messages, "success");
        this.fetchSequencingData();
      });
    },
    handleAnalysisSizeChange(val) {
      this.analysis_query_form.page_size = val;
      this.fetchAnalysisData();
    },
    handleSequencingSizeChange(val) {
      this.sequencing_query_form.page_size = val;
      this.fetchSequencingData();
    },
    handleAnalysisCurrentChange(val) {
      this.analysis_query_form.page = val;
      this.fetchAnalysisData();
    },
    handleSequencingCurrentChange(val) {
      this.sequencing_query_form.page = val;
      this.fetchSequencingData();
    },
    handleAnalysisQuery() {
      this.analysis_query_form.page = 1;
      this.fetchAnalysisData();
    },
    handleSequencingQuery() {
      this.sequencing_query_form.page = 1;
      this.fetchSequencingData();
    },
    async fetchAnalysisData() {
      this.listLoading = true;
      const data = await getAnalysisTaskInterfaceList(this.analysis_query_form);
      this.analysisList = data.results;
      this.analysis_all_count = data.all_count;
      setTimeout(() => {
        this.listLoading = false;
      }, 500);
    },
    async fetchSequencingData() {
      this.listLoading = true;
      const data = await getSequencingTaskInterfaceList(
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
