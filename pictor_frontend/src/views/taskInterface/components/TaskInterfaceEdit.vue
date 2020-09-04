<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogFormVisible"
    width="800px"
    @close="close"
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="接口名称" prop="name">
        <el-input v-model.trim="form.name" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="接口域名" prop="domain">
        <el-input v-model.trim="form.domain" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="成功返回码" prop="success_code">
        <el-input
          v-model.trim="form.success_code"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="失败返回码" prop="error_code">
        <el-input v-model.trim="form.error_code" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="启动任务URI" prop="start_uri">
        <el-input v-model.trim="form.start_uri" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="停止任务URI" prop="stop_uri">
        <el-input v-model.trim="form.stop_uri" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="继续运行任务URI" prop="continue_uri">
        <el-input
          v-model.trim="form.continue_uri"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="重置任务URI" prop="reset_uri">
        <el-input v-model.trim="form.reset_uri" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="查询任务状态URI" prop="status_uri">
        <el-input v-model.trim="form.status_uri" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="获取任务结果URI" prop="result_uri">
        <el-input v-model.trim="form.result_uri" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="获取运行日志URI" prop="log_uri">
        <el-input v-model.trim="form.log_uri" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="是否启用该配置" prop="is_active">
        <el-checkbox v-model.trim="form.is_active"></el-checkbox>
      </el-form-item>
      <el-form-item label="项目描述/备注" prop="remark">
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
  createAnalysisTaskInterface,
  updateAnalysisTaskInterface,
  retrieveAnalysisTaskInterface,
} from "@/api/task_interface";

export default {
  name: "TaskInterfaceEdit",
  data() {
    return {
      form: {
        id: "",
        name: "假设接口",
        domain: "http://127.0.0.1:8000/analysis/",
        success_code: "200 ",
        error_code: "400",
        start_uri: "start",
        stop_uri: "stop",
        continue_uri: "continue",
        reset_uri: "reset",
        status_uri: "status",
        result_uri: "result",
        log_uri: "log",
        is_active: true,
        remark: "",
      },
      rules: {
        name: [{ required: true, trigger: "blur", message: "请输入接口名称" }],
        domain: [
          { required: true, trigger: "blur", message: "请输入接口域名" },
        ],
        success_code: [
          { required: true, trigger: "blur", message: "请输入成功返回码" },
        ],
        error_code: [
          { required: true, trigger: "blur", message: "请输入失败返回码" },
        ],
        start_uri: [
          { required: true, trigger: "blur", message: "请输入启动任务URI" },
        ],
        stop_uri: [
          { required: true, trigger: "blur", message: "请输入停止任务URI" },
        ],
        continue_uri: [
          { required: true, trigger: "blur", message: "请输入继续运行任务URI" },
        ],
        reset_uri: [
          { required: true, trigger: "blur", message: "请输入重置任务URI" },
        ],
        status_uri: [
          { required: true, trigger: "blur", message: "请输入查询任务状态URI" },
        ],
        result_uri: [
          { required: true, trigger: "blur", message: "请输入获取任务结果URI" },
        ],
        log_uri: [
          { required: true, trigger: "blur", message: "请输入获取运行日志URI" },
        ],
      },
      title: "",
      edit_type: "create",
      dialogFormVisible: false,
    };
  },
  created() {},
  methods: {
    showEdit(row) {
      if (!row) {
        this.title = "新增分析任务接口";
        this.edit_type = "create";
      } else {
        this.title = "编辑分析任务接口";
        this.edit_type = "update";
        this.detail(row.id);
      }
      this.dialogFormVisible = true;
    },
    async detail(instance_id) {
      const data = await retrieveAnalysisTaskInterface(instance_id);
      const results = data.results;
      this.form = Object.assign(
        {},
        {
          id: results.id,
          name: results.name,
          domain: results.domain,
          success_code: results.success_code,
          error_code: results.error_code,
          start_uri: results.start_uri,
          stop_uri: results.stop_uri,
          continue_uri: results.continue_uri,
          reset_uri: results.reset_uri,
          status_uri: results.status_uri,
          result_uri: results.result_uri,
          log_uri: results.log_uri,
          is_active: results.is_active,
          remark: results.remark,
        }
      );
    },
    close() {
      this.$refs["form"].resetFields();
      this.form = this.$options.data().form;
      this.dialogFormVisible = false;
      this.$emit("fetchData");
    },
    save() {
      this.$refs["form"].validate(async (valid) => {
        if (valid) {
          let data = {};
          if (this.edit_type === "create") {
            data = await createAnalysisTaskInterface(this.form);
          } else {
            data = await updateAnalysisTaskInterface(this.form.id, this.form);
          }
          const { messages, results } = data;
          this.$baseMessage(messages, "success");
          this.$refs["form"].resetFields();
          this.dialogFormVisible = false;
          this.$emit("fetchData");
          this.form = this.$options.data().form;
        } else {
          return false;
        }
      });
    },
  },
};
</script>
