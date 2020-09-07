<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogFormVisible"
    width="800px"
    @close="close"
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="模块来源" prop="module_type">
        <el-select v-model="form.module_type" placeholder="请选择模块来源">
          <el-option
            v-for="item in typeOptions"
            :key="item.key"
            :label="item.value"
            :value="item.key"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="模块名称" prop="name">
        <el-input v-model.trim="form.name"></el-input>
      </el-form-item>
      <el-form-item label="模块命令" prop="command">
        <el-input v-model.trim="form.command"></el-input>
      </el-form-item>
      <el-form-item
        v-if="form.module_type === 20"
        label="模块文件"
        prop="pipeline_file"
      >
        <el-upload
          ref="module_upload"
          v-model.trim="form.pipeline_file"
          :file-list="fileList"
          action=""
          accept=".tar, .zip, .rar"
          drag
          :multiple="false"
          :before-upload="beforeUpload"
          :on-change="handleFileChange"
          :on-remove="handleRemove"
          :on-preview="handlePreview"
          :http-request="save"
          :auto-upload="false"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <div slot="tip" class="el-upload__tip">
            只能上传压缩文件夹:tar/zip/rar，文件大小不能超过20M
          </div>
        </el-upload>
      </el-form-item>
      <el-form-item v-else label="链接路径" prop="url">
        <el-input v-model.trim="form.url" @blur="getVersionOptions"></el-input>
      </el-form-item>
      <el-form-item label="版本号/分支名" prop="version">
        <el-input
          v-if="form.module_type === 20"
          v-model.trim="form.version"
        ></el-input>
        <el-select
          v-else
          v-model="form.version"
          filterable
          placeholder="请选择版本号/分支名, 通过github获取分支需要时间, 请耐心等待"
        >
          <el-option
            v-for="item in versionOptions"
            :key="item"
            :label="item"
            :value="item"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="开发者" prop="developer">
        <el-input v-model.trim="form.developer"></el-input>
      </el-form-item>
      <el-form-item label="开发者邮箱" prop="email">
        <el-input v-model.trim="form.email"></el-input>
      </el-form-item>
      <el-form-item label="描述/备注" prop="remark">
        <el-input
          v-model.trim="form.remark"
          type="textarea"
          :autosize="{ minRows: 2, maxRows: 4 }"
        ></el-input>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">取 消</el-button>
      <el-button type="primary" @click="save">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script>
import {
  getAnalysisModuleTypes,
  createAnalysisModule,
  updateAnalysisModule,
  retrieveAnalysisModule,
  getAnalysisModuleVersions,
} from "@/api/analysisModule";
import { baseURL } from "@/config/settings";
import { isEmail } from "@/utils/validate";

export default {
  name: "AnalysisModuleEdit",
  data() {
    const validateEmail = (rule, value, callback) => {
      if (value && !isEmail(value)) {
        callback(new Error("邮箱格式不符合"));
      } else {
        callback();
      }
    };
    return {
      form: {
        module_type: 10,
        name: "",
        command: "nextflow run",
        url: "",
        pipeline_file: "",
        version: "",
        developer: "",
        email: "",
        remark: "",
      },
      typeOptions: [],
      versionOptions: [],
      is_file_change: false, // 是否更换文件
      fileList: [],
      title: "",
      edit_type: "create",
      dialogFormVisible: false,
      rules: {
        module_type: [
          { required: true, trigger: "blur", message: "请选择模块类型" },
        ],
        name: [{ required: true, trigger: "blur", message: "请输入模块名称" }],
        command: [
          { required: true, trigger: "blur", message: "请输入模块运行命令" },
        ],
        url: [
          {
            required: true,
            trigger: "blur",
            message: "请输入模块链接(git)",
          },
        ],
        pipeline_file: [
          {
            required: true,
            trigger: "blur",
            message: "请输入模块文件",
          },
        ],
        version: [
          { required: true, trigger: "blur", message: "请输入模块版本" },
        ],
        email: [
          {
            validator: validateEmail,
          },
        ],
      },
    };
  },
  computed: {},
  created() {
    this.getTypeOptions();
  },
  methods: {
    showEdit(row) {
      if (!row) {
        this.title = "新增模块";
        this.edit_type = "create";
        this.form = this.$options.data().form;
        this.versionOptions = [];
        this.fileList = [];
        this.is_file_change = false;
      } else {
        this.title = "编辑模块";
        this.edit_type = "update";
        this.detail(row.id);
      }
      this.dialogFormVisible = true;
    },
    close() {
      this.$refs["form"].resetFields();
      if (this.form.module_type === 20) {
        this.$refs["module_upload"].clearFiles();
      }
      this.form = this.$options.data().form;
      this.versionOptions = [];
      this.fileList = [];
      this.is_file_change = false;
      this.$emit("fetchData");
      this.dialogFormVisible = false;
    },
    async detail(instance_id) {
      const data = await retrieveAnalysisModule(instance_id);
      const results = data.results;
      this.form = Object.assign(
        {},
        {
          id: results.id,
          module_type: results.module_type,
          name: results.name,
          command: results.command,
          url: results.url,
          pipeline_file: results.pipeline_file,
          version: results.version,
          developer: results.developer,
          email: results.email,
          remark: results.remark,
        }
      );
      if (this.form.module_type === 10) {
        this.getVersionOptions();
      }
      if (this.form.module_type === 20) {
        this.fileList = [this.form.pipeline_file];
      }
    },
    async getTypeOptions() {
      const data = await getAnalysisModuleTypes();
      this.typeOptions = data.results;
    },
    async getVersionOptions() {
      console.log("getVersionOptions");
      if (this.form.url) {
        const data = await getAnalysisModuleVersions({
          module_url: this.form.url,
        });
        this.versionOptions = data.results;
      }
    },
    //上传文件，获取文件流
    handleFileChange(file) {
      this.form.pipeline_file = file.raw;
      this.fileList = [this.form.pipeline_file];
      this.is_file_change = true;
    },
    handleRemove(file, fileList) {
      this.form.pipeline_file = "";
    },
    handlePreview(file) {
      if (file.url) {
        const link = document.createElement("a");
        link.href = `${baseURL}${file.url}`;
        link.target = "_blank";
        document.body.appendChild(link);
        link.click();
        link.remove();
      }
    },
    beforeUpload(file) {},
    getFormData() {
      let index = this.form.pipeline_file.name.lastIndexOf(".");
      let suffix = this.form.pipeline_file.name.substr(index + 1);
      // 创建表单对象
      let formData = new FormData();
      // 后端接受参数 ，可以接受多个参数
      formData.append("pipeline_file", this.form.pipeline_file);
      formData.append("uploadFileName", this.form.pipeline_file.name);
      formData.append("uploadFileContentType", suffix);
      formData.append("module_type", this.form.module_type);
      formData.append("name", this.form.name);
      formData.append("command", this.form.command);
      formData.append("version", this.form.version);
      formData.append("developer", this.form.developer);
      formData.append("email", this.form.email);
      formData.append("remark", this.form.remark);
      return formData;
    },
    save() {
      this.$refs["form"].validate(async (valid) => {
        if (valid) {
          let data = {};
          if (this.edit_type === "create") {
            if (this.form.module_type === 20) {
              let formData = this.getFormData();
              data = await createAnalysisModule(formData, {
                "Content-Type": "multipart/form-data;charset=UTF-8",
              });
            } else {
              delete this.form.pipeline_file;
              data = await createAnalysisModule(this.form);
            }
          } else {
            if (this.form.module_type === 20) {
              if (!this.is_file_change) {
                delete this.form.pipeline_file;
                data = await updateAnalysisModule(this.form.id, this.form);
              } else {
                let formData = this.getFormData();
                data = await updateAnalysisModule(
                  this.form.id,
                  formData,
                  "put",
                  {
                    "Content-Type": "multipart/form-data;charset=UTF-8",
                  }
                );
              }
            } else {
              data = await updateAnalysisModule(this.form.id, this.form);
            }
          }
          const { messages, results } = data;
          this.$baseMessage(messages, "success");
          this.$refs["form"].resetFields();
          this.dialogFormVisible = false;
          this.$emit("listEvent");
          this.form = this.$options.data().form;
        } else {
          return false;
        }
      });
    },
  },
};
</script>
