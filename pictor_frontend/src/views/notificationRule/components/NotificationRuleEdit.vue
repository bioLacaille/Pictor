<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogFormVisible"
    width="800px"
    @close="close"
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="规则名称" prop="name">
        <el-input v-model.trim="form.name" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="是否发送站内信" prop="is_notify">
        <el-checkbox v-model.trim="form.is_notify"></el-checkbox>
      </el-form-item>
      <el-form-item label="是否发送邮件" prop="is_email">
        <el-checkbox v-model.trim="form.is_email"></el-checkbox>
      </el-form-item>
      <el-form-item label="是否使用SSL" prop="email_user_ssl">
        <el-checkbox v-model.trim="form.email_user_ssl"></el-checkbox>
      </el-form-item>
      <el-form-item label="发送邮箱服务器" prop="email_host">
        <el-input
          v-model.trim="form.email_host"
          autocomplete="off"
          placeholder="smtp.exmail.qq.com"
        ></el-input>
      </el-form-item>
      <el-form-item label="发送邮箱端口" prop="email_port">
        <el-input
          v-model.trim="form.email_port"
          autocomplete="off"
          placeholder="465"
        ></el-input>
      </el-form-item>
      <el-form-item label="发送邮箱帐号" prop="email_host_user">
        <el-input
          v-model.trim="form.email_host_user"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="发送邮箱密码" prop="email_host_password">
        <el-input
          v-model.trim="form.email_host_password"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="发件人名称" prop="email_from_title">
        <el-input
          v-model.trim="form.email_from_title"
          autocomplete="off"
          placeholder="Pictor <support@pictor.com.cn>"
        ></el-input>
      </el-form-item>
      <el-form-item label="通知等级" prop="info_level">
        <el-input v-model.trim="form.info_level" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="紧急等级" prop="urgent_level">
        <el-input
          v-model.trim="form.urgent_level"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="非常紧急等级" prop="very_urgent_level">
        <el-input
          v-model.trim="form.very_urgent_level"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="警告等级" prop="warning_level">
        <el-input
          v-model.trim="form.warning_level"
          autocomplete="off"
        ></el-input>
      </el-form-item>
      <el-form-item label="错误等级" prop="error_level">
        <el-input v-model.trim="form.error_level" autocomplete="off"></el-input>
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
  createNotificationRule,
  updateNotificationRule,
  retrieveNotificationRule,
} from "@/api/notificationRule";

export default {
  name: "NotificationRuleEdit",
  data() {
    return {
      form: {
        id: "",
        name: "",
        is_email: false,
        is_notify: true,
        email_user_ssl: true,
        email_host: "",
        email_port: "",
        email_host_user: "",
        email_host_password: "",
        email_from_title: "",
        info_level: "通知",
        urgent_level: "紧急",
        very_urgent_level: "非常紧急",
        warning_level: "警告",
        error_level: "错误",
        is_active: true,
        remark: "",
      },
      rules: {
        name: [{ required: true, trigger: "blur", message: "请输入规则名称" }],
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
        this.title = "新增消息规则";
        this.edit_type = "create";
      } else {
        this.title = "编辑消息规则";
        this.edit_type = "update";
        this.detail(row.id);
      }
      this.dialogFormVisible = true;
    },
    async detail(instance_id) {
      const data = await retrieveNotificationRule(instance_id);
      const results = data.results;
      this.form = Object.assign(
        {},
        {
          id: results.id,
          name: results.name,
          is_email: results.is_email,
          is_notify: results.is_notify,
          email_user_ssl: results.email_user_ssl,
          email_host: results.email_host,
          email_host_user: results.email_host_user,
          email_port: results.email_port,
          email_host_password: results.email_host_password,
          email_from_title: results.email_from_title,
          info_level: results.info_level,
          urgent_level: results.urgent_level,
          very_urgent_level: results.very_urgent_level,
          warning_level: results.warning_level,
          error_level: results.error_level,
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
            data = await createNotificationRule(this.form);
          } else {
            data = await updateNotificationRule(this.form.id, this.form);
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
