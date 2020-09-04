<template>
  <el-dialog
    append-to-body
    :title="title"
    :visible.sync="dialogFormVisible"
    width="80%"
    @close="close"
  >
    <div>
      <div>
        <div class="placeholder"></div>
        <el-steps :active="active" align-center finish-status="success">
          <el-step
            v-if="edit_type === 'create'"
            title="步骤1"
            description="选择分析模块"
          ></el-step>
          <el-step v-else title="步骤1" description="选择分析模块"></el-step>
          <el-step
            v-if="edit_type === 'create'"
            title="步骤2"
            description="填写分析参数"
          ></el-step>
          <el-step v-else title="步骤2" description="编辑分析参数"></el-step>
          <el-step
            v-if="edit_type === 'create'"
            title="步骤3"
            description="生成分析任务并启动"
          ></el-step>
          <el-step v-else title="步骤3" description="确认编辑"></el-step>
        </el-steps>
        <div>
          <div :style="{ display: firstDisplay }">
            <el-divider></el-divider>
            <div>
              <el-row :gutter="20">
                <el-col
                  v-for="(item, index) in analysisModuleList"
                  :key="index"
                  :xs="24"
                  :sm="8"
                  :md="8"
                  :lg="8"
                  :xl="4"
                >
                  <el-card shadow="hover" style="height: 280px;">
                    <div
                      slot="header"
                      style="text-align: center; cursor: pointer;"
                      @click="handleSelectModule(item)"
                    >
                      <el-popover
                        v-if="item.remark"
                        trigger="hover"
                        placement="top"
                      >
                        <p>{{ item.remark }}</p>
                        <div slot="reference" class="name-wrapper">
                          <h1>
                            <el-tag size="medium">
                              {{ item.name }}
                            </el-tag>
                          </h1>
                        </div>
                      </el-popover>
                      <h1 v-else>
                        <el-tag size="medium">
                          {{ item.name }}
                        </el-tag>
                      </h1>
                      <el-tag type="success">{{
                        moduleTypeNameFilter(item.module_type)
                      }}</el-tag>
                    </div>
                    <div
                      style="text-align: center; cursor: pointer;"
                      @click="handleSelectModule(item)"
                    >
                      <font-awesome-layers full-width class="fa-4x">
                        <font-awesome-icon
                          icon="tablet"
                          :style="{ color: '#ADD8E6' }"
                          size="lg"
                        />
                        <font-awesome-layers-text
                          transform="down-0 right-1 shrink-12"
                          :value="item.version"
                          style="
                            color: black;
                            font-size: 0.8em;
                            text-align: center;
                            word-break: initial;
                          "
                        />
                      </font-awesome-layers>
                      <br />
                      <br />
                      <div class="tip">
                        <el-alert
                          v-if="analysis_module_instance.id === item.id"
                          type="success"
                          :closable="false"
                          center
                        >
                          已选
                        </el-alert>
                        <el-alert v-else type="info" :closable="false" center>
                          点击选择
                        </el-alert>
                      </div>
                    </div>
                    <br />
                  </el-card>
                </el-col>
              </el-row>
              <el-pagination
                :background="background"
                :current-page="page"
                :layout="layout"
                :page-size="page_size"
                :total="all_count"
                @current-change="handleCurrentChange"
                @size-change="handleSizeChange"
              ></el-pagination>
            </div>
          </div>
          <div :style="{ display: secondDisplay }">
            <el-divider></el-divider>
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
            <div>
              <el-form
                ref="analysis-form"
                :model="form"
                :rules="rules"
                label-width="140px"
              >
                <br />
                <el-divider content-position="center">
                  <i class="el-icon-mobile-phone"></i
                  ><el-tag type="primary">基本信息录入</el-tag>
                </el-divider>
                <el-form-item
                  label="所属项目"
                  prop="project"
                  class="center_div"
                >
                  <el-select
                    v-model="form.project"
                    placeholder="请选择所属项目"
                    :disabled="
                      edit_type === 'update' && project_instance.id !== ''
                    "
                    @change="handleSelectProject($event)"
                  >
                    <el-option
                      v-for="item in projectOptions"
                      :key="item.id"
                      :label="`${item.name}\(${item.serial_number}\)`"
                      :value="item.id"
                    />
                  </el-select>
                </el-form-item>
                <el-form-item
                  label="任务编号"
                  prop="serial_number"
                  class="center_div"
                >
                  <el-input
                    v-model.trim="form.serial_number"
                    :disabled="edit_type === 'update'"
                    autocomplete="off"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="是否发送通知"
                  prop="is_email"
                  class="center_div"
                >
                  <el-switch v-model.trim="form.is_email"></el-switch>
                </el-form-item>
                <el-form-item
                  label="通知邮箱地址"
                  prop="email_list"
                  class="center_div"
                >
                  <el-input
                    v-model.trim="form.email_list"
                    autocomplete="off"
                    placeholder="多个邮箱使用逗号(,)或分号(;)分割"
                  ></el-input>
                </el-form-item>
                <br />
                <el-divider content-position="center">
                  <i class="el-icon-mobile-phone"></i
                  ><el-tag type="primary">运行命令</el-tag>
                </el-divider>
                <el-form-item
                  label="运行命令"
                  prop="email_list"
                  class="center_div"
                >
                  <el-input
                    v-model.trim="form.command"
                    placeholder="运行命令"
                  ></el-input>
                </el-form-item>
                <br />
                <br />
                <el-divider content-position="center">
                  <i class="el-icon-mobile-phone"></i
                  ><el-tag type="primary">分析参数设置</el-tag>
                </el-divider>
                <el-card shadow="hover" style="height: 80px;">
                  <div class="flexWrap center_div">
                    <div class="flexLeft" style="padding-right: 15%;">
                      <el-button type="primary" @click="handleSaveParameter"
                        >保存当前参数</el-button
                      >
                    </div>
                    <div class="flexRight" style="width: 85%;">
                      <el-select
                        v-model="parameter_instance"
                        placeholder="请选择参数方案"
                        @change="handleSelectParameter"
                      >
                        <el-option
                          v-for="item in parameterOptions"
                          :key="item.id"
                          :label="item.name"
                          :value="item.id"
                        />
                      </el-select>
                    </div>
                  </div>
                </el-card>
                <div class="command center_div" style="height: 120px;">
                  <p style="margin-top: 1.3%;">$ > {{ full_command }}</p>
                </div>
                <el-form
                  v-for="(parameter, index) of parameter_input_list"
                  :ref="'parameter' + index"
                  :key="index"
                  :model="parameter"
                  :rules="parameter_rules"
                  label-width="140px"
                >
                  <div class="flexWrap center_div textCenter">
                    <div class="flexLeft">
                      <el-select
                        v-model.trim="parameter.command_tag"
                        placeholder="命令符"
                        @change="setFullCommand"
                      >
                        <el-option label="--" value="--"></el-option>
                        <el-option label="-" value="-"></el-option>
                        <el-option label="无" value=""></el-option>
                      </el-select>
                    </div>
                    <div class="flexWrap flexRight">
                      <div class="flexLeft">
                        <el-input
                          v-model.trim="parameter.parameter_key"
                          autocomplete="off"
                          placeholder="参数"
                          @blur="setFullCommand"
                        ></el-input>
                      </div>
                      <div class="flexWrap flexRight">
                        <div class="reverseFlexLeft">
                          <el-input
                            v-model.trim="parameter.parameter_value"
                            autocomplete="off"
                            placeholder="参数值"
                            @blur="setFullCommand"
                            @change="setFullCommand"
                          ></el-input>
                        </div>
                        <div class="reverseFlexRight">
                          <div class="flexWrap">
                            <div style="width: 50%;">
                              <el-tooltip
                                class="item"
                                effect="dark"
                                content="选择数据"
                                placement="top-start"
                              >
                                <el-button
                                  type="success"
                                  icon="el-icon-data-analysis"
                                  @click="handleSelectData(index)"
                                ></el-button>
                              </el-tooltip>
                            </div>
                            <div style="width: 40%; padding-left: 20%;">
                              <el-tooltip
                                class="item"
                                effect="dark"
                                content="删除参数"
                                placement="top-start"
                              >
                                <el-button
                                  type="danger"
                                  icon="el-icon-delete"
                                  @click="handleRemoveParameter(index)"
                                ></el-button>
                              </el-tooltip>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <br />
                </el-form>
                <div class="flexWrap center_div textCenter">
                  <div style="width: 96%;">
                    <el-button
                      class="dk-btn-block is-ghost flexRight"
                      size="small"
                      type="info"
                      plain
                      icon="el-icon-plus"
                      @click="handleAddParameter"
                      >新增参数</el-button
                    >
                  </div>
                </div>
              </el-form>
              <br />
              <br />
            </div>
          </div>
          <div class="elp-step-third" :style="{ display: thirdDisplay }">
            <div class="elp-step-success-icon">
              <i class="el-icon-circle-check"></i>
            </div>
            <div class="elp-step-success-info">
              请确认任务信息, 任务结果请留意站内信或邮件通知!
            </div>
            <div class="elp-step-success-card">
              <div>
                <strong>所属项目编号：</strong>
                <span>{{ project_instance.serial_number }}</span>
              </div>
              <div>
                <strong>所属项目名称：</strong>
                <span>{{ project_instance.name }}</span>
              </div>
              <div>
                <strong>任务编号： </strong>
                <span>{{ form.serial_number }}</span>
              </div>
              <div>
                <strong>是否发送通知：</strong>
                <span>{{ form.is_email }}</span>
              </div>
              <div>
                <strong>接收通知邮箱地址： </strong>
                <span>{{ form.email_list }}</span>
              </div>
              <div>
                <strong>运行命令： </strong>
                <span>{{ full_command }}</span>
              </div>
            </div>
          </div>
        </div>
        <el-divider></el-divider>
        <div class="elp-button">
          <el-button
            v-if="active > 1"
            style="margin-top: 12px;"
            type="primary"
            @click="prev"
            >上一步</el-button
          >
          <el-button
            v-if="active < 3 && active > 1"
            style="margin-top: 12px;"
            type="info"
            @click="next"
            >下一步</el-button
          >
          <el-button
            v-if="active === 3 && edit_type === 'create'"
            style="margin-top: 12px;"
            type="success"
            @click="save(false)"
            >新增</el-button
          >
          <el-button
            v-if="active === 3 && edit_type === 'create'"
            style="margin-top: 12px;"
            type="warning"
            @click="save(true)"
            >新增并启动</el-button
          >
          <el-button
            v-if="active === 3 && edit_type === 'update'"
            style="margin-top: 12px;"
            type="success"
            @click="update"
            >修 改</el-button
          >
        </div>
      </div>
    </div>
    <save-parameter
      ref="parameter"
      @saveParameter="saveParameter"
    ></save-parameter>
    <select-dataset
      ref="dataset"
      @setParameterValue="setParameterValue"
    ></select-dataset>
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
  startAnalysis,
} from "@/api/analysis";
import { getProjectList, retrieveProject } from "@/api/project";
import SaveParameter from "./SaveParameter";
import SelectDataset from "./SelectDataset";

export default {
  name: "AddAnalysis",
  components: {
    SaveParameter,
    SelectDataset,
  },
  data() {
    return {
      dialogFormVisible: false,
      // 步骤
      active: 1,
      firstDisplay: "block",
      secondDisplay: "none",
      thirdDisplay: "none",
      analysisModuleList: [], // 分析模块
      listLoading: true,
      page: 1,
      page_size: 50,
      layout: "total, sizes, prev, pager, next, jumper",
      all_count: 0,
      background: true,
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
      form: {
        id: "",
        analysis_module: "",
        analysis_parameter: "",
        project: "",
        serial_number: "",
        command: "",
        is_email: false,
        email_list: "",
      },
      parameter_input_list: [
        {
          command_tag: "--",
          parameter_key: "",
          parameter_value: "",
        },
      ],
      full_command: "",
      projectOptions: [],
      parameter_instance: null,
      parameterOptions: [],
      moduleTypeMap: {},
      rules: {
        project: [
          { required: true, trigger: "change", message: "请选择所属项目" },
        ],
        serial_number: [
          { required: true, trigger: "blur", message: "请输入分析编号" },
        ],
      },
      parameter_rules: {
        command_tag: [
          { required: true, trigger: "blur", message: "请选择命令符" },
        ],
        parameter_key: [
          { required: true, trigger: "blur", message: "请输入参数" },
        ],
        parameter_value: [
          { required: true, trigger: "blur", message: "请输入参数值" },
        ],
      },
      edit_type: "create",
      title: "新增分析任务",
    };
  },
  watch: {
    analysis_module_instance(val) {
      if (val) {
        this.listParameterOptions();
      }
    },
  },
  created() {
    this.getModuleTypeFilter();
  },
  methods: {
    show(row) {
      if (row) {
        this.edit_type = "update";
        this.fetchAnalysisModules();
        this.listProjectOptions();
        this.getAnalysisDetail(row.id);
        this.title = "编辑分析任务";
        this.active = 2;
        this.firstDisplay = "none";
        this.secondDisplay = "block";
        this.thirdDisplay = "none";
        this.dialogFormVisible = true;
      } else {
        this.title = "新增分析任务";
        this.edit_type = "create";
        this.fetchAnalysisModules();
        this.dialogFormVisible = true;
      }
    },
    close() {
      this.analysis_module_instance = {
        id: "",
        name: "",
        version: "",
        command: "",
        module_type: "",
        file_uri: "",
        remark: "",
      };
      this.form = {
        id: "",
        analysis_module: "",
        analysis_parameter: "",
        project: "",
        serial_number: "",
        command: "",
        is_email: false,
        email_list: "",
      };
      this.project_instance = {
        id: "",
        serial_number: "",
        name: "",
      };
      this.parameter_input_list = [
        {
          command_tag: "--",
          parameter_key: "",
          parameter_value: "",
        },
      ];
      this.full_command = "";
      this.projectOptions = [];
      this.parameterOptions = [];
      this.active = 1;
      this.firstDisplay = "block";
      this.secondDisplay = "none";
      this.thirdDisplay = "none";
      this.$refs["analysis-form"].resetFields();
      this.dialogFormVisible = false;
    },
    moduleTypeNameFilter(val) {
      console.log("moduleTypeNameFilter", this.moduleTypeMap);
      return this.moduleTypeMap[val];
    },
    async getModuleTypeFilter() {
      const data = await getAnalysisModuleTypes();
      for (let i = 0; i < data.results.length; i++) {
        this.moduleTypeMap[data.results[i].key] = data.results[i].value;
      }
    },
    showStep() {
      console.log("this.active", this.active);
      if (this.active === 1) {
        this.firstDisplay = "block";
        this.secondDisplay = "none";
        this.thirdDisplay = "none";
      }
      if (this.active === 2) {
        this.firstDisplay = "none";
        this.secondDisplay = "block";
        this.thirdDisplay = "none";
      }
      if (this.active === 3) {
        this.firstDisplay = "none";
        this.secondDisplay = "none";
        this.thirdDisplay = "block";
      }
    },
    next() {
      console.log("next active", this.active);
      if (this.active === 2) {
        let valid = true;
        this.$refs["analysis-form"].validate(async (form_valid) => {
          if (!form_valid) {
            this.$baseMessage("请输入任务必填项", "error");
            valid = false;
          }
        });
        if (this.parameter_input_list.length <= 0) {
          this.$baseMessage("请至少输入一行参数", "error");
          valid = false;
        }
        if (this.parameter_input_list.length === 1) {
          if (
            this.parameter_input_list[0].parameter_key === null ||
            this.parameter_input_list[0].parameter_key === ""
          ) {
            this.$baseMessage("请输入参数", "error");
            valid = false;
          }
        }
        if (valid) {
          this.active++;
          this.showStep();
        }
      } else {
        this.active++;
        this.showStep();
      }
    },
    prev() {
      this.active--;
      this.showStep();
    },
    // 获取分析模块
    async fetchAnalysisModules() {
      this.listLoading = true;
      const data = await getAnalysisModuleList({
        page: this.page,
        page_size: this.page_size,
      });
      this.analysisModuleList = data.results;
      this.all_count = data.all_count;
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
    // 选择分析模块
    handleSelectModule(item) {
      this.moduleDetail(item.id);
      this.listProjectOptions();
      this.setFullCommand();
      this.next();
    },
    async listProjectOptions() {
      const data = await getProjectList({ not_page: true });
      this.projectOptions = data.results;
    },
    async listParameterOptions() {
      console.log("listParameterOptions", this.analysis_module_instance);
      const data = await getAnalysisParameterList({
        not_page: true,
        analysis_module_id: this.analysis_module_instance.id,
      });
      this.parameterOptions = data.results;
    },
    handleRemoveParameter(index) {
      console.log("handleRemoveParameter index", index);
      this.parameter_input_list.splice(index, 1);
      this.setFullCommand();
    },
    async moduleDetail(instance_id) {
      const data = await retrieveAnalysisModule(instance_id);
      const results = data.results;
      this.analysis_module_instance = Object.assign(
        {},
        {
          id: results.id,
          name: results.name,
          version: results.version,
          command: results.command,
          module_type: results.module_type,
          file_uri: results.file_uri,
          remark: results.remark,
        }
      );
      this.form.command = results.command;
    },
    setFullCommand() {
      this.full_command = `${this.form.command} ${this.analysis_module_instance.file_uri} `;
      for (let i = 0; i < this.parameter_input_list.length; i++) {
        if (
          this.parameter_input_list[i].parameter_key !== null &&
          this.parameter_input_list[i].parameter_key !== ""
        ) {
          this.full_command = `${this.full_command}
        ${this.parameter_input_list[i].command_tag}${this.parameter_input_list[i].parameter_key}
        ${this.parameter_input_list[i].parameter_value}`;
        }
      }
    },
    handleSaveParameter() {
      this.$refs["parameter"].showEdit();
    },
    async saveParameter(name, remark) {
      if (this.parameter_input_list.length <= 0) {
        this.$baseMessage("请至少输入一行参数", "error");
        return;
      }
      if (this.parameter_input_list.length === 1) {
        if (
          this.parameter_input_list[0].parameter_key === null ||
          this.parameter_input_list[0].parameter_key === ""
        ) {
          this.$baseMessage("请输入参数", "error");
          return;
        }
      }
      const data = await createAnalysisParameter({
        module: this.analysis_module_instance.id,
        name: name,
        detail: JSON.stringify(this.parameter_input_list),
        remark: remark,
      });
      const { messages, results } = data;
      this.$baseMessage(messages, "success");
      this.listParameterOptions();
      this.form.analysis_parameter = results.id;
    },
    handleSelectData(parameter_index) {
      this.$refs["dataset"].showSelectData(parameter_index);
    },
    setParameterValue(index, value) {
      this.parameter_input_list[index].parameter_value = value;
      this.setFullCommand();
    },
    handleAddParameter() {
      this.parameter_input_list.push({
        command_tag: "--",
        parameter_key: "",
        parameter_value: "",
      });
    },
    async handleSelectParameter(item) {
      const data = await retrieveAnalysisParameter(item);
      this.parameter_input_list = data.results.detail;
      this.setFullCommand();
    },
    async handleSelectProject(item) {
      console.log("handleSelectProject", item);
      const data = await retrieveProject(item);
      this.project_instance = data.results;
    },
    handleSizeChange(val) {
      this.page_size = val;
      this.fetchData();
    },
    handleCurrentChange(val) {
      this.page = val;
      this.fetchData();
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
      this.parameter_input_list = results.analysis_parameter;
      console.log("parameter_input_list", this.parameter_input_list);
      this.form = Object.assign(
        {},
        {
          id: results.id,
          analysis_module: analysis_module_id,
          analysis_parameter: results.analysis_parameter,
          project: project_id,
          serial_number: results.serial_number,
          command: results.command,
          is_email: results.is_email,
          email_list: results.email_list,
        }
      );
      this.setFullCommand();
    },
    async save(start = false) {
      this.form.analysis_module = this.analysis_module_instance.id;
      this.form.analysis_parameter = JSON.stringify(this.parameter_input_list);
      const data = await createAnalysis(this.form);
      const { messages, results } = data;
      if (start) {
        await startAnalysis(results.id);
      }
      this.$baseMessage(messages, "success");
      this.$emit("fetchData");
      this.close();
    },
    async update() {
      this.form.analysis_module = this.analysis_module_instance.id;
      this.form.analysis_parameter = JSON.stringify(this.parameter_input_list);
      const data = await updateAnalysis(this.form.id, this.form);
      const { messages, results } = data;
      this.$baseMessage(messages, "success");
      this.$emit("fetchData");
      this.close();
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
