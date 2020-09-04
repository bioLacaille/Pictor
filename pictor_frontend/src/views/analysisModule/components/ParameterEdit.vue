<template>
  <el-dialog
    append-to-body
    :title="title"
    :visible.sync="dialogFormVisible"
    width="60%"
    @close="close"
  >
    <div class="command center_div" style="height: 120px;">
      <p style="margin-top: 1.3%;">$ > {{ full_command }}</p>
    </div>
    <el-form ref="form" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="模块名称" prop="name">
        <el-input v-model.trim="form.name"></el-input>
      </el-form-item>
      <el-form-item label="描述/备注" prop="remark">
        <el-input
          v-model.trim="form.remark"
          type="textarea"
          :autosize="{ minRows: 2, maxRows: 4 }"
        ></el-input>
      </el-form-item>
    </el-form>
    <br />
    <el-divider content-position="center">
      <i class="el-icon-mobile-phone"></i
      ><el-tag type="primary">参数设置</el-tag>
    </el-divider>
    <el-form
      v-for="(parameter, index) of parameter_input_list"
      :ref="'parameter' + index"
      :key="index"
      :model="parameter"
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
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">取 消</el-button>
      <el-button type="primary" @click="save">确 定</el-button>
    </div>
    <select-dataset
      ref="dataset"
      @setParameterValue="setParameterValue"
    ></select-dataset>
  </el-dialog>
</template>

<script>
import {
  createAnalysisParameter,
  updateAnalysisParameter,
  retrieveAnalysisParameter,
} from "@/api/analysisParameter";
import SelectDataset from "../../analysis/components/SelectDataset";

export default {
  name: "ParameterEdit",
  components: {
    SelectDataset,
  },
  data() {
    return {
      title: "",
      edit_type: "create",
      dialogFormVisible: false,
      full_command: "",
      form: {
        id: "",
        name: "",
        remark: "",
      },
      parameter_input_list: [
        {
          command_tag: "--",
          parameter_key: "",
          parameter_value: "",
        },
      ],
      module: {
        id: "",
        name: "",
        version: "",
        command: "",
        module_type: "",
        remark: "",
      },
      rules: {
        name: [{ required: true, trigger: "blur", message: "请输入模块名称" }],
      },
    };
  },
  computed: {},
  watch: {
    parameter_input_list(val) {
      this.setFullCommand();
    },
  },
  created() {},
  methods: {
    showEdit(row, module) {
      this.module = module;
      if (!row) {
        this.title = "新增参数方案";
        this.edit_type = "create";
        this.form = this.$options.data().form;
      } else {
        this.title = "编辑参数方案";
        this.edit_type = "update";
        this.detail(row.id);
      }
      this.setFullCommand();
      this.dialogFormVisible = true;
    },
    close() {
      this.$refs["form"].resetFields();
      this.form = this.$options.data().form;
      this.module = {
        id: "",
        name: "",
        version: "",
        command: "",
        module_type: "",
        remark: "",
      };
      this.parameter_input_list = [
        {
          command_tag: "--",
          parameter_key: "",
          parameter_value: "",
        },
      ];
      // this.$emit("fetchData");
      this.dialogFormVisible = false;
    },
    handleRemoveParameter(index) {
      this.parameter_input_list.splice(index, 1);
      this.setFullCommand();
    },
    handleAddParameter() {
      this.parameter_input_list.push({
        command_tag: "--",
        parameter_key: "",
        parameter_value: "",
      });
    },
    handleSelectData(parameter_index) {
      this.$refs["dataset"].showSelectData(parameter_index);
    },
    setParameterValue(index, value) {
      this.parameter_input_list[index].parameter_value = value;
      this.setFullCommand();
    },
    async detail(instance_id) {
      const data = await retrieveAnalysisParameter(instance_id);
      const results = data.results;
      this.form = Object.assign(
        {},
        {
          id: results.id,
          name: results.name,
          remark: results.remark,
        }
      );
      this.parameter_input_list = results.detail;
    },
    setFullCommand() {
      this.full_command = `${this.module.command} `;
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
    save() {
      this.$refs["form"].validate(async (valid) => {
        if (valid) {
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
          this.form["module"] = this.module.id;
          this.form["detail"] = JSON.stringify(this.parameter_input_list);
          let data = {};
          if (this.edit_type === "create") {
            data = await createAnalysisParameter(this.form);
          } else {
            data = await updateAnalysisParameter(this.form.id, this.form);
          }
          const { messages, results } = data;
          this.$baseMessage(messages, "success");
          this.close();
        } else {
          return false;
        }
      });
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
