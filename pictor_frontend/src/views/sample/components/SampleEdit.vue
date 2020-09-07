<template>
  <el-dialog
    append-to-body
    :title="title"
    :visible.sync="dialogFormVisible"
    width="800px"
    @close="close"
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="所属项目" prop="project">
        <el-select v-model="form.project" placeholder="请选择所属项目">
          <el-option
            v-for="item in projectOptions"
            :key="item.id"
            :label="`${item.name}\(${item.serial_number}\)`"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="样本编号" prop="serial_number">
        <el-input
          v-model.trim="form.serial_number"
          :disabled="edit_type === 'update'"
        ></el-input>
      </el-form-item>
      <el-form-item label="样本名称" prop="sample_name">
        <el-input v-model.trim="form.sample_name" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="样本类型" prop="sample_type">
        <el-input v-model.trim="form.sample_type" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="样本来源" prop="sample_source">
        <el-input
          v-model.trim="form.sample_source"
          autocomplete="off"
        ></el-input>
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
import { createSample, updateSample, retrieveSample } from "@/api/sample";
import { getProjectList } from "@/api/project";
import { getSampleSerialNumber } from "@/api/serialNumberSetting";

export default {
  name: "ProjectEdit",
  data() {
    return {
      form: {
        project: "",
        serial_number: "",
        sample_name: "",
        sample_type: "",
        sample_source: "",
        remark: "",
      },
      rules: {
        serial_number: [
          { required: true, trigger: "blur", message: "请输入样本编号" },
        ],
        sample_name: [
          { required: true, trigger: "blur", message: "请输入样本名称" },
        ],
        project: [{ required: true, trigger: "blur", message: "请选择项目" }],
      },
      projectOptions: [],
      title: "",
      edit_type: "create",
      dialogFormVisible: false,
    };
  },
  created() {
    this.listProjectOptions();
  },
  methods: {
    async listProjectOptions() {
      const data = await getProjectList({ not_page: true });
      this.projectOptions = data.results;
    },
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
      const data = await retrieveSample(instance_id);
      const results = data.results;
      this.form = Object.assign(
        {},
        {
          id: results.id,
          project: results.project.id,
          serial_number: results.serial_number,
          sample_name: results.sample_name,
          sample_type: results.sample_type,
          sample_source: results.sample_source,
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
      const data = await getSampleSerialNumber();
      this.form.serial_number = data.results;
    },
    save() {
      this.$refs["form"].validate(async (valid) => {
        if (valid) {
          let data = {};
          if (this.edit_type === "create") {
            data = await createSample(this.form);
          } else {
            data = await updateSample(this.form.id, this.form);
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
