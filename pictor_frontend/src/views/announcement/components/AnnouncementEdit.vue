<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogFormVisible"
    width="800px"
    @close="close"
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="公告标题" prop="title">
        <el-input v-model.trim="form.title" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="是否发布" prop="is_publish">
        <el-checkbox v-model.trim="form.is_publish"></el-checkbox>
      </el-form-item>
      <el-form-item label="跳转链接" prop="link">
        <el-input v-model.trim="form.link" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="公告内容" prop="content">
        <el-input
          v-model.trim="form.content"
          type="textarea"
          :autosize="{ minRows: 2, maxRows: 4 }"
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
  createAnnouncement,
  updateAnnouncement,
  retrieveAnnouncement,
} from "@/api/announcement";

export default {
  name: "AnnouncementEdit",
  data() {
    return {
      form: {
        id: "",
        title: "",
        link: "",
        content: "",
        is_publish: true,
        remark: "",
      },
      rules: {
        title: [{ required: true, trigger: "blur", message: "请输入公告标题" }],
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
        this.title = "新增公告";
        this.edit_type = "create";
      } else {
        this.title = "编辑公告";
        this.edit_type = "update";
        this.detail(row.id);
      }
      this.dialogFormVisible = true;
    },
    async detail(instance_id) {
      const data = await retrieveAnnouncement(instance_id);
      const results = data.results;
      this.form = Object.assign(
        {},
        {
          id: results.id,
          title: results.title,
          link: results.link,
          content: results.content,
          is_publish: results.is_publish,
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
            data = await createAnnouncement(this.form);
          } else {
            data = await updateAnnouncement(this.form.id, this.form);
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
