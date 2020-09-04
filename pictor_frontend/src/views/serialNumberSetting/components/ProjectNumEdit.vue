<template>
  <el-dialog
    :title="title"
    :visible.sync="projectNumFormVisible"
    width="800px"
    @close="close"
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="规则名称" prop="name">
        <el-input v-model.trim="form.name" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="前缀字符" prop="start_string">
        <el-input
          v-model.trim="form.start_string"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="中间字符生成长度" prop="middle_string_len">
        <el-input-number
          v-model.trim="form.middle_string_len"
          autocomplete="off"
        ></el-input-number>
      </el-form-item>
      <el-form-item label="后缀字符" prop="end_string">
        <el-input v-model.trim="form.end_string" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="分割字符" prop="spilt_string">
        <el-input
          v-model.trim="form.spilt_string"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="是否启用该配置" prop="is_active">
        <el-checkbox v-model.trim="form.is_active"></el-checkbox>
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
  createProjectSerialNumberSetting,
  updateProjectSerialNumberSetting,
  retrieveProjectSerialNumberSetting,
} from "@/api/serialNumberSetting";

export default {
  name: "ProjectNumEdit",
  data() {
    return {
      form: {
        id: "",
        name: "",
        start_string: "project",
        middle_string_len: 6,
        end_string: "",
        spilt_string: "-",
        is_active: true,
        remark: "",
      },
      rules: {
        name: [{ required: true, trigger: "blur", message: "请输入接口名称" }],
      },
      title: "",
      edit_type: "create",
      projectNumFormVisible: false,
    };
  },
  created() {},
  methods: {
    showEdit(row) {
      if (!row) {
        this.title = "新增项目编号规则";
        this.edit_type = "create";
      } else {
        this.title = "编辑项目编号规则";
        this.edit_type = "update";
        this.detail(row.id);
      }
      this.projectNumFormVisible = true;
    },
    async detail(instance_id) {
      const data = await retrieveProjectSerialNumberSetting(instance_id);
      const results = data.results;
      this.form = Object.assign(
        {},
        {
          id: results.id,
          name: results.name,
          start_string: results.start_string,
          middle_string_len: results.middle_string_len,
          end_string: results.end_string,
          spilt_string: results.spilt_string,
          is_active: results.is_active,
          remark: results.remark,
        }
      );
    },
    close() {
      this.$refs["form"].resetFields();
      this.form = this.$options.data().form;
      this.projectNumFormVisible = false;
    },
    save() {
      this.$refs["form"].validate(async (valid) => {
        if (valid) {
          let data = {};
          if (this.edit_type === "create") {
            data = await createProjectSerialNumberSetting(this.form);
          } else {
            data = await updateProjectSerialNumberSetting(
              this.form.id,
              this.form
            );
          }
          const { messages, results } = data;
          this.$baseMessage(messages, "success");
          this.$refs["form"].resetFields();
          this.projectNumFormVisible = false;
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
