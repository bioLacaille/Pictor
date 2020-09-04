<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogFormVisible"
    width="800px"
    @close="close"
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="任务编号" prop="serial_number">
        <el-input v-model.trim="form.serial_number"></el-input>
      </el-form-item>
      <el-form-item label="批次编号" prop="batch_number">
        <el-select v-model="form.batch_number" placeholder="请选择批次编号">
          <el-option
            v-for="item in batchNumberOptions"
            :key="item"
            :label="item"
            :value="item"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="sample_sheet" prop="sample_sheet">
        <el-input
          v-model.trim="form.sample_sheet"
          autocomplete="off"
          type="file"
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
import {
  createSequencing,
  updateSequencing,
  retrieveSequencing,
} from "@/api/sequencing";

export default {
  name: "SequencingEdit",
  data() {
    return {
      form: {
        serial_number: "",
        batch_number: "",
        sample_sheet: "",
        remark: "",
      },
      rules: {
        serial_number: [
          { required: true, trigger: "blur", message: "请输入任务编号" },
        ],
        batch_number: [
          { required: true, trigger: "blur", message: "请选择批次编号" },
        ],
        sample_sheet: [
          { required: true, trigger: "blur", message: "请上传sample_sheet" },
        ],
      },
      title: "",
      edit_type: "create",
      dialogFormVisible: false,
      batchNumberOptions: ["test1", "test2", "test3"],
    };
  },
  created() {},
  methods: {
    showEdit(row) {
      if (!row) {
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
      const data = await retrieveSequencing(instance_id);
      const results = data.results;
      this.form = Object.assign(
        {},
        {
          id: results.id,
          serial_number: results.serial_number,
          batch_number: results.batch_number,
          sample_sheet: results.sample_sheet,
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
            data = await createSequencing(this.form);
          } else {
            data = await updateSequencing(this.form.id, this.form);
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
