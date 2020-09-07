<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogFormVisible"
    width="800px"
    @close="close"
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="项目编号" prop="serial_number">
        <el-input
          v-model.trim="form.serial_number"
          :disabled="edit_type === 'update'"
        ></el-input>
      </el-form-item>
      <el-form-item label="项目名称" prop="name">
        <el-input v-model.trim="form.name" autocomplete="off"></el-input>
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
import { createProject, updateProject, retrieveProject } from "@/api/project";
import { getProjectSerialNumber } from "@/api/serialNumberSetting";

export default {
  name: "ProjectEdit",
  data() {
    return {
      form: {
        serial_number: "",
        name: "",
        remark: "",
      },
      rules: {
        serial_number: [
          { required: true, trigger: "blur", message: "请输入项目编号" },
        ],
        name: [{ required: true, trigger: "blur", message: "请输入项目名称" }],
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
        this.get_number();
        this.title = "添加";
        this.edit_type = "create";
      } else {
        this.title = "编辑";
        this.edit_type = "update";
        this.detail(row.id);
      }
      this.dialogFormVisible = true;
    },
    async detail(instance_id) {
      const data = await retrieveProject(instance_id);
      const results = data.results;
      this.form = Object.assign(
        {},
        {
          id: results.id,
          serial_number: results.serial_number,
          name: results.name,
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
    async get_number() {
      const data = await getProjectSerialNumber();
      this.form.serial_number = data.results;
    },
    save() {
      this.$refs["form"].validate(async (valid) => {
        if (valid) {
          let data = {};
          if (this.edit_type === "create") {
            data = await createProject(this.form);
          } else {
            data = await updateProject(this.form.id, this.form);
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
