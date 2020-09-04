<template>
  <!--文件路径操作区-->
  <div v-if="dataSearchVisible" id="data_header" class="wl-explorer">
    <el-form :inline="true" class="wl-header-file" @submit.native.prevent>
      <el-form-item class="file-path-box">
        <el-autocomplete
          ref="file-path-ipt"
          v-model="path_search"
          class="u-full"
          placeholder="请输入文件路径"
          :fetch-suggestions="pathQuerySearch"
          @keyup.enter.native="filterPathChange"
          @select="filterPathChange"
        >
          <img
            slot="prefix"
            class="file-path-img"
            src="../Explorer/images/folder@3x.png"
            alt="文件夹"
            title="文件夹"
          />
        </el-autocomplete>
      </el-form-item>
      <el-form-item class="file-search-box">
        <el-input
          v-model="key_search"
          placeholder="请输入关键字搜索"
          @keyup.enter.native="filterSearch()"
        >
          <el-button
            slot="append"
            icon="el-icon-search file-search"
            @click="filterSearch()"
          ></el-button>
        </el-input>
      </el-form-item>
      <el-form-item class="file-handle-box">
        <i
          class="iconfont icon-wl-left file-path-handle"
          :class="{ 'u-disabled': !pathIsPrv }"
          @click="pathBtn('prv')"
        ></i>
        <i
          class="iconfont icon-wl-right file-path-handle"
          :class="{ 'u-disabled': !pathIsNext }"
          @click="pathBtn('next')"
        ></i>
        <i
          class="iconfont icon-wl-up file-path-handle"
          @click="pathBtn('top')"
        ></i>
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
    </el-form>
  </div>
</template>

<script>
import { getDataDirectoryPath } from "@/api/dataset";
export default {
  name: "Index",
  props: {
    dataSearchVisible: {
      type: Boolean,
      default: false,
    },
    // 数据类型
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
  },
  data() {
    return {
      path_search: "", // 路径搜索
      key_search: "", // 关键字搜索
      // 记录路径历史
      prv_path: [],
      next_path: [],
      top_path: "",
    };
  },
  computed: {
    // 是否存在上一层
    pathIsPrv() {
      return this.prv_path.length > 0;
    },
    // 是否存在下一层
    pathIsNext() {
      return this.next_path.length > 0;
    },
  },
  watch: {
    currentPath(val, old) {
      this.path_search = val;
      this.prv_path.push(old);
    },
    dataType(val) {
      this.path_search = "";
      this.next_path = [];
      this.prv_path = [];
    },
  },
  created() {
    this.setTopPath();
  },
  methods: {
    setTopPath() {
      this.top_path = this.currentPath;
      this.path_search = this.currentPath;
    },
    // 地址输入框匹配
    async pathQuerySearch(queryString, cb) {
      console.log("queryString", queryString);
      const data = await getDataDirectoryPath({
        data_type: this.dataType,
        current_path: this.currentPath,
        query_path: queryString,
      });
      this.path_search = queryString;
      // 调用 callback 返回建议列表的数据
      cb(data.results);
    },
    // 输入文件路径
    async filterPathChange(item) {
      const prv_path = this.currentPath;
      const data = await getDataDirectoryPath({
        valid: true,
        data_type: this.dataType,
        current_path: this.currentPath,
        query_path: this.path_search,
      });
      if (data.success) {
        this.$emit(
          "getFileList",
          this.dataType,
          this.path_search,
          this.key_search
        );
        this.prv_path.push(prv_path);
      }
    },
    // 搜索文件
    filterSearch() {
      this.$emit(
        "getFileList",
        this.dataType,
        this.path_search,
        this.key_search
      );
    },
    // 前进后退按钮操作
    pathBtn(type) {
      console.log("pathBtn type", type);
      if (type === "prv") {
        if (!this.pathIsPrv) return;
        const prv_path = this.prv_path.pop();
        const current_path = this.currentPath;
        this.$emit("getFileList", this.dataType, prv_path);
        this.path_search = prv_path;
        this.next_path.push(current_path);
      } else if (type === "next") {
        if (!this.pathIsNext) return;
        const next_path = this.next_path.pop();
        const current_path = this.currentPath;
        this.$emit("getFileList", this.dataType, next_path);
        this.path_search = next_path;
        this.prv_path.push(current_path);
      } else {
        this.next_path = [];
        this.prv_path = [];
        this.$emit("getFileList", this.dataType, this.top_path);
        this.path_search = this.top_path;
      }
    },
    changeForShowList(show_list) {
      this.$emit("changeShowList", show_list);
    },
  },
};
</script>

<style scoped></style>
