<template>
  <el-dialog
    append-to-body
    title="保存参数方案"
    :visible.sync="dialogFormVisible"
    width="800px"
    @close="close"
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="方案名称" prop="name">
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
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">取 消</el-button>
      <el-button type="primary" @click="save">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: "SaveParameter",
  data() {
    return {
      form: {
        name: "",
        remark: "",
      },
      rules: {
        name: [
          { required: true, trigger: "blur", message: "请输入参数方案名称" },
        ],
      },
      dialogFormVisible: false,
    };
  },
  created() {},
  methods: {
    showEdit() {
      this.dialogFormVisible = true;
      this.$forceUpdate();
    },
    close() {
      this.$refs["form"].resetFields();
      this.form = this.$options.data().form;
      this.dialogFormVisible = false;
    },
    save() {
      this.$refs["form"].validate(async (valid) => {
        if (valid) {
          this.$emit("saveParameter", this.form.name, this.form.remark);
          this.$refs["form"].resetFields();
          this.dialogFormVisible = false;
          this.form = this.$options.data().form;
        } else {
          return false;
        }
      });
    },
  },
};
</script>
