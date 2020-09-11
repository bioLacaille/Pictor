<template>
  <el-dialog
    :title="title"
    :visible.sync="dialogFormVisible"
    width="800px"
    @close="close"
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="用户角色" prop="role_level">
        <el-select v-model="form.role_level" placeholder="请选择用户角色">
          <el-option
            v-for="(item, key, index) in role_level_options"
            :key="index"
            :label="item"
            :value="parseInt(key)"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="用户账号" prop="username">
        <el-input
          v-model.trim="form.username"
          placeholder="请输入用户账号"
          :disabled="edit_type === 'update'"
        ></el-input>
      </el-form-item>
      <el-form-item
        v-if="edit_type === 'create'"
        label="账号密码"
        prop="password"
      >
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
          ><font-awesome-icon :icon="['fas', 'eye-slash']"
        /></span>
        <span v-else class="show-pwd" @click="showPwd"
          ><font-awesome-icon :icon="['fas', 'eye']"
        /></span>
      </el-form-item>
      <el-form-item label="用户昵称" prop="nickname">
        <el-input
          v-model.trim="form.nickname"
          placeholder="请输入用户昵称"
        ></el-input>
      </el-form-item>
      <el-form-item label="用户邮箱" prop="email">
        <el-input
          v-model.trim="form.email"
          placeholder="请输入用户邮箱"
        ></el-input>
      </el-form-item>
      <el-form-item label="用户性别" prop="gender">
        <el-select v-model="form.gender" placeholder="请选择用户性别">
          <el-option label="男" value="男"></el-option>
          <el-option label="女" value="女"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="电话号码" prop="phone">
        <el-input
          v-model.trim="form.phone"
          placeholder="请输入电话号码"
        ></el-input>
      </el-form-item>
      <el-form-item label="职称" prop="title">
        <el-input v-model.trim="form.title" placeholder="请输入职称"></el-input>
      </el-form-item>
      <el-form-item label="地址" prop="address">
        <el-input
          v-model.trim="form.address"
          placeholder="请输入地址"
        ></el-input>
      </el-form-item>
      <el-form-item label="描述/备注" prop="remark">
        <el-input
          v-model.trim="form.remark"
          type="textarea"
          placeholder="请输入描述/备注"
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
  createUser,
  updateUser,
  retrieveUser,
  getRoleLevels,
} from "@/api/user";
import { isEmail, isPhone, isPassword } from "@/utils/validate";

export default {
  name: "UserEdit",
  data() {
    const validatePassword = (rule, value, callback) => {
      if (!isPassword(value)) {
        callback(new Error("密码不能少于6位"));
      } else {
        callback();
      }
    };
    const validateEmail = (rule, value, callback) => {
      if (!isEmail(value)) {
        callback(new Error("邮箱格式不符合"));
      } else {
        callback();
      }
    };
    const validatePhone = (rule, value, callback) => {
      if (value && !isPhone(value)) {
        callback(new Error("电话格式不符合"));
      } else {
        callback();
      }
    };
    return {
      form: {
        username: "",
        password: "",
        nickname: "",
        email: "",
        gender: "男",
        phone: "",
        title: "",
        address: "",
        remark: "",
        role_level: 10,
      },
      rules: {
        role_level: [
          { required: true, trigger: "blur", message: "请输入用户角色等级" },
        ],
        username: [
          { required: true, trigger: "blur", message: "请输入用户账号" },
        ],
        password: [
          {
            required: true,
            trigger: "blur",
            validator: validatePassword,
          },
        ],
        nickname: [
          { required: true, trigger: "blur", message: "请输入用户昵称" },
        ],
        email: [
          {
            required: true,
            trigger: "blur",
            validator: validateEmail,
          },
        ],
        phone: [{ validator: validatePhone }],
      },
      role_level_options: [],
      title: "",
      edit_type: "create",
      dialogFormVisible: false,
      passwordType: "password",
    };
  },
  created() {
    this.getRoleLevelOptions();
  },
  methods: {
    showPwd() {
      this.passwordType === "password"
        ? (this.passwordType = "")
        : (this.passwordType = "password");
      this.$nextTick(() => {
        this.$refs.password.focus();
      });
    },
    showEdit(row) {
      if (!row) {
        this.title = "新增用户";
        this.edit_type = "create";
      } else {
        this.title = "编辑用户";
        this.edit_type = "update";
        this.detail(row.id);
      }
      this.dialogFormVisible = true;
    },
    async detail(instance_id) {
      const data = await retrieveUser(instance_id);
      const results = data.results;
      this.form = Object.assign(
        {},
        {
          id: results.id,
          username: results.username,
          nickname: results.nickname,
          email: results.email,
          gender: results.gender,
          phone: results.phone,
          title: results.title,
          address: results.address,
          remark: results.remark,
          role_level: results.role_level,
        }
      );
    },
    async getRoleLevelOptions() {
      const data = await getRoleLevels({ zh: true });
      this.role_level_options = data.results;
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
            data = await createUser(this.form);
          } else {
            data = await updateUser(this.form.id, this.form);
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
