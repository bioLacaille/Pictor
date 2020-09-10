<template>
  <!-- 头部按钮区 -->
  <div v-if="dataHeaderVisible" id="data_header" class="wl-explorer">
    <el-form class="wl-header-btn" :inline="true" @submit.native.prevent>
      <el-form-item>
        <el-button type="success" @click="showUpload">上传文件</el-button>
        <el-button type="primary" @click="handleFolder">新增文件夹</el-button>
        <el-button
          type="danger"
          :disabled="checkedFiles.length <= 0"
          @click="handleDel"
          >删除</el-button
        >
        <el-button type="info">离线上传(todo)</el-button>
        <slot name="header-btn"></slot>
      </el-form-item>
      <el-form-item>
        <el-dropdown trigger="click" placement="bottom">
          <el-button type="primary" plain>
            更多操作
            <i class="el-icon-arrow-down el-icon--right"></i>
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item
              :disabled="!(checkedFiles.length === 1)"
              @click.native="handleRename"
              >重命名</el-dropdown-item
            >
            <el-dropdown-item
              :disabled="checkedFiles.length <= 0"
              @click.native="handleCopy"
              >复制(todo)</el-dropdown-item
            >
            <el-dropdown-item command="cut">移动(todo)</el-dropdown-item>
            <slot name="header-dropdown"></slot>
          </el-dropdown-menu>
        </el-dropdown>
      </el-form-item>
      <el-form-item v-show="uploading.ing">
        <span>正在上传：</span>
        <span class="c-blue u-uploading-name">{{ uploading.name }}</span>
        <span class="c-blue">({{ uploading.percentage }}%)</span>
      </el-form-item>
      <el-form-item class="u-right">
        <i
          v-show="showList"
          class="iconfont icon-wl-list file-show-type"
          @click="changeForShowList(!showList)"
        ></i>
        <i
          v-show="!showList"
          class="iconfont icon-wl-grid file-show-type"
          @click="changeForShowList(!showList)"
        ></i>
      </el-form-item>
      <data-name-edit
        ref="d-edit"
        @getForFileList="getForFileList"
      ></data-name-edit>
      <!--      <data-copy ref="d-copy" @getForFileList="getForFileList"></data-copy>-->
    </el-form>
  </div>
</template>

<script>
import DataNameEdit from "./cores/DataNameEdit";
import DataCopy from "./cores/DataCopy";
import store from "@/store";
import { bulkDeleteDataSet } from "@/api/dataset";
export default {
  name: "DataHeader",
  components: {
    DataNameEdit,
    // DataCopy,
  },
  props: {
    dataHeaderVisible: {
      type: Boolean,
      default: false,
    },
    dataType: {
      type: Number,
      default: 10,
    },
    currentPath: {
      type: String,
      default: "",
    },
    showList: {
      type: Boolean,
      default: false,
    },
    checkedFiles: {
      type: Array,
      default() {
        return [];
      },
    },
  },
  data() {
    return {
      uploading: {
        name: "",
        percentage: 0,
        ing: false,
      }, // 当前上传文件状态
    };
  },
  computed: {},
  watch: {},
  created() {},
  methods: {
    getForFileList() {
      console.log("getForFileList222222222222222222222");
      this.$emit("getFileList");
    },
    changeForShowList(show_list) {
      this.$emit("changeShowList", show_list);
    },
    // 新增文件夹
    handleFolder() {
      console.log("handleFolder");
      this.$refs["d-edit"].showEdit(this.dataType, this.currentPath, null);
    },
    // 重命名
    handleRename() {
      let selected_file = null;
      if (this.checkedFiles.length > 0) {
        selected_file = this.checkedFiles[0];
      }
      this.$refs["d-edit"].showEdit(
        this.dataType,
        this.currentPath,
        selected_file
      );
    },
    // 复制
    handleCopy() {
      const ids = this.checkedFiles.map((item) => item.id);
      this.$refs["d-copy"].showEdit(ids);
    },
    // 删除
    async handleDel() {
      if (this.checkedFiles.length > 0) {
        const ids = this.checkedFiles.map((item) => item.id);
        this.$baseConfirm("你确定要删除选中文件吗", null, async () => {
          const data = await bulkDeleteDataSet({ deleted_objects: ids });
          const messages = data.messages;
          this.$baseMessage(messages, "success");
          this.$emit("getFileList");
        });
      } else {
        this.$baseMessage("未选中任何文件", "error");
        return false;
      }
    },
    // 上传文件
    showUpload() {
      store.dispatch("uploader/setUploadState", true);
      store.dispatch("uploader/setDataType", this.dataType);
      store.dispatch("uploader/setCurrentPath", this.currentPath);
    },
  },
};
</script>
