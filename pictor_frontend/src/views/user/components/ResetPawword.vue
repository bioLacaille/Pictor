<template>
  <el-dialog
    title="重置密码"
    :visible.sync="dialogFormVisible"
    width="800px"
    @close="close"
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="新密码" prop="password">
        <el-input
          key="password"
          ref="password"
          v-model.trim="form.password"
          :type="passwordType"
          auto-complete="off"
          placeholder="请输入账号密码"
        />
        <span
          v-if="passwordType === 'password'"
          class="show-pwd"
          @click="showPwd"
          ><af-icon :icon="['fas', 'eye-slash']"
        /></span>
        <span v-else class="show-pwd" @click="showPwd"
          ><af-icon :icon="['fas', 'eye']"
        /></span>
      </el-form-item>
      <el-form-item label="确认密码" prop="confirm_password">
        <el-input
          key="confirm_password"
          ref="confirm_password"
          v-model.trim="form.confirm_password"
          :type="confirmPasswordType"
          auto-complete="off"
          placeholder="请输入账号密码"
        />
        <span
          v-if="confirmPasswordType === 'password'"
          class="show-pwd"
          @click="showConfirmPwd"
          ><af-icon :icon="['fas', 'eye-slash']"
        /></span>
        <span v-else class="show-pwd" @click="showConfirmPwd"
          ><af-icon :icon="['fas', 'eye']"
        /></span>
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">取 消</el-button>
      <el-button type="primary" @click="save">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { resetPasswordUser } from "@/api/user";
import { isPassword } from "@/utils/validate";

export default {
  name: "ResetPassword",
  data() {
    const validatePassword = (rule, value, callback) => {
      if (!isPassword(value)) {
        callback(new Error("密码不能少于6位"));
      } else {
        callback();
      }
    };
    return {
      form: {
        id: "",
        password: "",
        confirm_password: "",
      },
      rules: {
        password: [
          {
            required: true,
            trigger: "blur",
            validator: validatePassword,
          },
        ],
        confirm_password: [
          {
            required: true,
            trigger: "blur",
            validator: validatePassword,
          },
        ],
      },
      dialogFormVisible: false,
      passwordType: "password",
      confirmPasswordType: "password",
    };
  },
  created() {},
  methods: {
    showPwd() {
      this.passwordType === "password"
        ? (this.passwordType = "")
        : (this.passwordType = "password");
      this.$nextTick(() => {
        this.$refs.password.focus();
      });
    },
    showConfirmPwd() {
      this.confirmPasswordType === "password"
        ? (this.confirmPasswordType = "")
        : (this.confirmPasswordType = "password");
      this.$nextTick(() => {
        this.$refs.confirm_password.focus();
      });
    },
    showEdit(row) {
      this.form.id = row.id;
      this.dialogFormVisible = true;
    },
    close() {
      this.$refs["form"].resetFields();
      this.form = this.$options.data().form;
      this.dialogFormVisible = false;
    },
    save() {
      this.$refs["form"].validate(async (valid) => {
        if (valid) {
          if (this.form.password !== this.form.confirm_password) {
            this.$baseMessage("两次密码不一致!请重新输入!", "error");
            return false;
          }
          const data = await resetPasswordUser(this.form.id, this.form);
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
.show-pwd {
  position: absolute;
  right: 10px;
  font-size: 16px;
  color: $base-font-color;
  cursor: pointer;
  user-select: none;
}
</style>
