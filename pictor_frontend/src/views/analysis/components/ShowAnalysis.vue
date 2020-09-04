<template>
  <el-dialog
    ref="showAnalysis"
    append-to-body
    title="分析任务信息"
    :visible.sync="dialogShowVisible"
    width="80%"
    @close="close"
  >
    <div class="table-container">
      <el-tabs v-model="currentTab" @tab-click="changeTab">
        <el-tab-pane key="info" label="任务信息" name="info">
          <div id="module">
            <el-divider content-position="center">
              <i class="el-icon-mobile-phone"></i
              ><el-tag type="primary">模块信息</el-tag>
            </el-divider>
            <div class="center_div textCenter">
              <font-awesome-layers full-width class="fa-4x">
                <font-awesome-icon
                  icon="tasks"
                  :style="{ color: '#ADD8E6' }"
                  size="lg"
                />
              </font-awesome-layers>
              <h1 style="margin-left: 100px;">
                {{ analysis_module_instance.name }}
              </h1>
              <h1 style="margin-left: 100px;">
                {{ analysis_module_instance.version }}
              </h1>
              <h1 style="margin-left: 100px;">
                {{ moduleTypeNameFilter(analysis_module_instance.module_type) }}
              </h1>
            </div>
            <el-divider></el-divider>
            <div class="center_div textCenter">
              <el-alert
                type="success"
                center
                :closable="false"
                :description="analysis_module_instance.remark"
              >
              </el-alert>
              <br />
            </div>
          </div>
          <br />
          <div id="info">
            <el-divider content-position="center">
              <i class="el-icon-mobile-phone"></i
              ><el-tag type="primary">基础信息</el-tag>
            </el-divider>
            <div class="elp-desc-list center_div">
              <div class="elp-desc-list-row">
                <div class="row-item">
                  <h4>任务编号：</h4>
                  <span>{{ analysis.serial_number }}</span>
                </div>
                <div class="row-item">
                  <h4>所属项目：</h4>
                  <span
                    >{{ project_instance.serial_number }} ({{
                      project_instance.name
                    }})</span
                  >
                </div>
                <div class="row-item">
                  <h4>创建者：</h4>
                  <span>{{ analysis.creator.nickname }}</span>
                </div>
              </div>
              <div class="elp-desc-list-row">
                <div class="row-item">
                  <h4>是否发送邮件：</h4>
                  <span>{{ analysis.is_email }}</span>
                </div>
              </div>
              <div class="elp-desc-list-row">
                <div class="row-item">
                  <h4>通知邮箱地址：</h4>
                  <span>{{ analysis.email_list }}</span>
                </div>
              </div>
              <div class="elp-desc-list-row">
                <div class="row-item">
                  <h4>运命命令：</h4>
                  <span>{{ analysis.command }}</span>
                </div>
              </div>
            </div>
            <div class="elp-desc-list">
              <div class="elp-desc-list-head">分析参数</div>
              <code-editor
                ref="full_command"
                :read-only="true"
                :value="full_command"
                :height="0"
                :width="width"
              ></code-editor>
            </div>
          </div>
          <div id="status">
            <el-divider content-position="center">
              <i class="el-icon-mobile-phone"></i
              ><el-tag type="primary">运行状态</el-tag>
            </el-divider>
            <div class="elp-desc-list center_div">
              <div class="elp-desc-list-row">
                <div class="row-item">
                  <el-progress
                    v-if="analysis.process"
                    type="circle"
                    :percentage="analysis.process"
                    status="success"
                  ></el-progress>
                  <el-progress
                    v-else
                    type="circle"
                    :percentage="0"
                  ></el-progress>
                </div>
                <div style="width: 100%;">
                  <h4>当前状态：</h4>
                  <el-tag :type="StatusTagFilter(analysis.status)">
                    <p>{{ statusOptions[analysis.status] }}</p>
                  </el-tag>
                </div>
                <div style="width: 100%;">
                  <div class="row-item">
                    <h4>启动时间：</h4>
                    <span>{{ analysis.started_time }}</span>
                  </div>
                  <div class="row-item">
                    <h4>结束时间：</h4>
                    <span>{{ analysis.finished_time }}</span>
                  </div>
                </div>
              </div>
              <div class="elp-desc-list-row">
                <div class="row-item"></div>
                <div class="row-item"></div>
              </div>
              <div class="elp-desc-list-row"></div>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane key="log" label="运行日志" name="log">
          <code-editor
            :value="running_logs"
            :height="height"
            :width="width"
          ></code-editor>
        </el-tab-pane>
        <el-tab-pane key="result" label="任务结果" name="result">
          <dataset
            ref="analysis-dataset"
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
import {
  getAnalysisModuleList,
  retrieveAnalysisModule,
} from "@/api/analysisModule";
import {
  getAnalysisParameterList,
  createAnalysisParameter,
  retrieveAnalysisParameter,
} from "@/api/analysisParameter";
import { getAnalysisModuleTypes } from "@/api/analysisModule";
import {
  createAnalysis,
  retrieveAnalysis,
  updateAnalysis,
  getAnalysisStatusList,
  getAnalysisLogs,
} from "@/api/analysis";
import { getProjectList, retrieveProject } from "@/api/project";
import SaveParameter from "./SaveParameter";
import SelectDataset from "./SelectDataset";
import CodeEditor from "@/components/CodeEditor/index";
import AddAnalysis from "./AddAnalysis";
import Dataset from "@/components/DataSet"; // 导入文件管理器

export default {
  name: "ShowAnalysis",
  components: {
    CodeEditor,
    Dataset,
  },
  data() {
    return {
      currentTab: "info",
      dialogShowVisible: false,
      analysis_module_instance: {
        id: "",
        name: "",
        version: "",
        command: "",
        module_type: "",
        file_uri: "",
        remark: "",
      },
      project_instance: {
        id: "",
        serial_number: "",
        name: "",
      },
      analysis: {
        id: "",
        analysis_module: "",
        analysis_parameter: "",
        project: "",
        serial_number: "",
        command: "",
        is_email: false,
        email_list: "",
        started_time: "",
        finished_time: "",
        status: "",
        process: "",
        creator: "",
      },
      parameter_input_list: [
        {
          command_tag: "--",
          parameter_key: "",
          parameter_value: "",
        },
      ],
      full_command: "",
      moduleTypeMap: {},
      statusOptions: {},
      running_logs: "22222222222222",
      width:
        window.innerWidth ||
        document.documentElement.clientWidth ||
        document.body.clientWidth,
      height:
        window.innerHeight ||
        document.documentElement.clientHeight ||
        document.body.clientHeight,
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
    };
  },
  watch: {},
  created() {
    this.getModuleTypeFilter();
    this.getAnalysisStatus();
  },
  methods: {
    show(row) {
      this.width = this.width * 0.75;
      this.height = this.height * 0.6;
      this.getAnalysisDetail(row.id);
      this.dialogShowVisible = true;
    },
    close() {
      this.dialogShowVisible = false;
    },
    async getAnalysisDetail(instance_id) {
      const data = await retrieveAnalysis(instance_id);
      const results = data.results;
      let analysis_module_id = null;
      let project_id = null;
      if (results.analysis_module) {
        this.analysis_module_instance = results.analysis_module;
        analysis_module_id = results.analysis_module.id;
      }
      if (results.project) {
        this.project_instance = results.project;
        project_id = results.project.id;
      }
      console.log(
        "getAnalysisDetail analysis_module_instance",
        this.analysis_module_instance
      );
      console.log("getAnalysisDetail project", this.project_instance);
      this.parameter_input_list = results.analysis_parameter;
      this.analysis = Object.assign(
        {},
        {
          id: results.id,
          analysis_module: analysis_module_id,
          analysis_parameter: results.analysis_parameter,
          project: project_id,
          serial_number: results.serial_number,
          command: results.command,
          is_email: results.is_email,
          creator: results.creator,
          started_time: results.started_time,
          finished_time: results.finished_time,
          status: results.status,
          process: results.process,
          email_list: results.email_list,
        }
      );
      this.setFullCommand();
    },
    setFullCommand() {
      this.full_command = `${this.analysis.command} ${this.analysis_module_instance.file_uri} `;
      for (let i = 0; i < this.parameter_input_list.length; i++) {
        if (
          this.parameter_input_list[i].parameter_key !== null &&
          this.parameter_input_list[i].parameter_key !== ""
        ) {
          this.full_command = `${this.full_command}\n${this.parameter_input_list[i].command_tag}${this.parameter_input_list[i].parameter_key} ${this.parameter_input_list[i].parameter_value}`;
        }
      }
    },
    moduleTypeNameFilter(val) {
      console.log(val, this.moduleTypeMap, this.moduleTypeMap[val]);
      return this.moduleTypeMap[val];
    },
    async getModuleTypeFilter() {
      const data = await getAnalysisModuleTypes();
      for (let i = 0; i < data.results.length; i++) {
        this.moduleTypeMap[data.results[i].key] = data.results[i].value;
      }
      console.log("getModuleTypeFilter", this.moduleTypeMap);
    },
    async getAnalysisStatus() {
      this.listLoading = true;
      const data = await getAnalysisStatusList();
      this.statusOptions = data.results;
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
    async getLogs() {
      this.listLoading = true;
      const data = await getAnalysisLogs(this.analysis.id);
      this.running_logs = data.results;
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
    changeTab(obj, e) {
      console.log("changeTab", obj.$vnode.key);
      if (obj.$vnode.key === "info") {
        console.log("changeTab", obj.$vnode.key);
        this.getAnalysisDetail(this.analysis.id);
      }
      if (obj.$vnode.key === "log") {
        console.log("changeTab", obj.$vnode.key);
        this.getLogs();
      }
      if (obj.$vnode.key === "result") {
        console.log("result", obj.$vnode.key);
        this.dataType = 30; // 项目数据
        this.currentPath = ""; // 分析数据路径
      }
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
.placeholder {
  height: 40px;
}
.command {
  padding: 8px 16px;
  background-color: #ecf8ff;
  border-radius: 4px;
  border-left: 5px solid #50bfff;
  margin: 20px 0;
}
.center_div {
  width: 90%;
  margin-left: 3%;
}
.textCenter {
  text-align: center;
  display: flex;
  flex-wrap: wrap;
  margin: 0 auto;
}
.flexWrap {
  display: flex;
  flex-wrap: wrap;
}
.flexLeft {
  width: 10%;
}
.reverseFlexLeft {
  width: 88%;
  padding-right: 2%;
}
.flexRight {
  width: 90%;
}
.reverseFlexRight {
  width: 10%;
}
</style>
