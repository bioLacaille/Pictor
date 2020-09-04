<template>
  <el-dialog
    :title="title"
    :visible.sync="DataNameVisible"
    width="800px"
    @close="close"
  >
    <el-form v-if="edit" ref="form" :model="form" label-width="120px">
      <el-form-item label="所在位置" prop="data_path">
        <span>{{ form.file_uri }}</span>
      </el-form-item>
    </el-form>
    <el-form
      v-if="edit && form.file_type === 10"
      ref="form"
      :model="form"
      label-width="120px"
    >
      <el-form-item label="文件大小" prop="file_size">
        <span>{{ form.file_size }}</span>
      </el-form-item>
    </el-form>
    <el-form v-if="edit" ref="form" :model="form" label-width="120px">
      <el-form-item label="创建时间" prop="created_time">
        <span>{{ form.created_time }}</span>
      </el-form-item>
    </el-form>
    <el-form v-if="edit" ref="form" :model="form" label-width="120px">
      <el-form-item label="修改时间" prop="edit_time">
        <span>{{ form.edit_time }}</span>
      </el-form-item>
    </el-form>
    <el-form
      v-if="edit && form.download_url"
      ref="form"
      :model="form"
      label-width="120px"
    >
      <el-form-item label="线上链接" prop="download_url">
        <span>{{ form.download_url }}</span>
      </el-form-item>
    </el-form>
    <el-form ref="form" :model="form" :rules="rules" label-width="120px">
      <el-form-item label="文件名称" prop="file_name">
        <el-input v-model.trim="form.file_name" autocomplete="off"></el-input>
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
  createDirectoryDataSet,
  updateDataSet,
  retrieveDataSet,
} from "@/api/dataset";

export default {
  name: "DataNameEdit",
  props: {},
  data() {
    return {
      data_type: 10, // 文件类型
      current_path: "", // todo当前路径
      form: {
        file_name: "",
      },
      rules: {
        file_name: [
          { required: true, trigger: "blur", message: "请输入文件夹名称" },
        ],
      },
      title: "",
      edit: false,
      DataNameVisible: false,
    };
  },
  created() {},
  methods: {
    showEdit(data_type, current_path, row) {
      this.data_type = data_type;
      this.current_path = current_path;
      if (!row) {
        this.title = "新建文件夹";
        this.edit = false;
      } else {
        this.title = "编辑文件夹名称";
        this.edit = true;
        this.detail(row.id);
      }
      this.DataNameVisible = true;
    },
    formatterSize(row) {
      const _GB = 1024 * 1024 * 1024; // GB
      const _MB = 1024 * 1024;
      const _KB = 1024; // GB
      if (row.file_size === null || row.file_type === 20) return "-";
      if (row.file_size < _KB) {
        return row.file_size + "B";
      }
      if (row.file_size > _KB && row.file_size < _MB) {
        let _kb = (row.file_size / _KB).toFixed(2);
        return parseFloat(_kb) + "KB";
      }
      if (row.file_size > _MB && row.file_size < _GB) {
        let _mb = (row.file_size / _MB).toFixed(2);
        return parseFloat(_mb) + "MB";
      }
      let _gb = (row.file_size / _GB).toFixed(2);
      return parseFloat(_gb) + "GB";
    },
    async detail(instance_id) {
      const data = await retrieveDataSet(instance_id);
      const results = data.results;
      this.form = Object.assign(
        {},
        {
          id: results.id,
          serial_number: results.serial_number,
          file_uri: results.file_uri,
          file_name: results.file_name,
          data_type: results.data_type,
          file_type: results.file_type,
          file_size: this.formatterSize(results),
          download_url: results.download_url,
          created_time: results.created_time,
          edit_time: results.edit_time,
        }
      );
    },
    close() {
      this.$refs["form"].resetFields();
      this.form = this.$options.data().form;
      this.DataNameVisible = false;
    },
    save() {
      const _that = this;
      this.$refs["form"].validate(async (valid) => {
        if (valid) {
          let data = {};
          _that.form["data_type"] = _that.data_type;
          _that.form["current_path"] = _that.current_path;
          if (!_that.edit) {
            data = await createDirectoryDataSet(this.form);
          } else {
            data = await updateDataSet(this.form.id, this.form);
          }
          const { messages, results } = data;
          _that.$baseMessage(messages, "success");
          _that.$refs["form"].resetFields();
          _that.DataNameVisible = false;
          _that.form = this.$options.data().form;
          _that.$emit("getForFileList");
        } else {
          return false;
        }
      });
    },
  },
};
</script>
