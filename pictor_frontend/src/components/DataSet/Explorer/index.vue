<template>
  <div v-if="dataExplorerVisible" class="wl-explorer">
    <!-- 主内容区 -->
    <el-scrollbar class="wl-main-scroll">
      <!-- 文件列表区 -->
      <div class="wl-main-list">
        <!-- 表格型文件列表 @selection-change="filterChecked" -->
        <el-table
          v-show="showList"
          ref="wl-table"
          highlight-current-row
          :border="showBorder"
          :data="data"
          class="wl-table"
          @select="filterChecked"
        >
          <el-table-column
            v-if="showCheckbox"
            align="center"
            type="selection"
            width="55"
          ></el-table-column>
          <el-table-column
            v-if="showIndex"
            align="center"
            type="index"
            label="序号"
            width="55"
          ></el-table-column>
          <slot name="table-column-top"></slot>
          <el-table-column
            v-for="i of selfColumns"
            :key="i._id"
            show-overflow-tooltip
            :prop="i.prop"
            :width="i.width"
            :label="i.label"
            :fixed="i.fixed"
            :align="i.align"
            :sort-by="i.sortBy"
            :sortable="i.sortable"
            :min-width="i.minWidth"
            :formatter="i.formatter"
            :column-key="i.columnKey"
            :class-name="i.className"
            :sort-method="i.sortMethod"
            :header-align="i.headerAlign"
            :render-header="i.renderHeader"
            :label-class-name="i.labelClassName"
          >
            <template slot-scope="scope">
              <!-- 非名称列 显示值-->
              <template v-if="i.prop !== selfProps.name">
                {{
                  i.formatter
                    ? i.formatter(
                        scope.row,
                        scope.column,
                        scope.row[i.prop],
                        scope.$index
                      )
                    : scope.row[i.prop]
                }}
              </template>
              <!-- 名称列 显示图标 -->
              <div
                v-else
                class="wl-name-col wl-is-folder"
                @click="clickDataFile(scope.row, scope.row[selfIsFolder])"
              >
                <!-- 不同文件类型图标区 -->
                <div class="namecol-iconbox">
                  <img
                    :src="fileTypeIcon(scope.row)"
                    class="name-col-icon"
                    alt="文件类型图标"
                  />
                </div>
                <!-- 不同文件类型 显示内容-->
                <div class="namecol-textbox">
                  {{
                    i.formatter
                      ? i.formatter(
                          scope.row,
                          scope.column,
                          scope.row[i.prop],
                          scope.$index
                        )
                      : scope.row[i.prop]
                  }}
                </div>
              </div>
            </template>
          </el-table-column>
          <slot name="table-column-bottom"></slot>
        </el-table>
        <!-- 列表型文件列表 -->
        <ul v-show="!showList" class="wl-list">
          <li
            v-for="(i, idx) in data"
            :key="i.id"
            class="wl-list-item wl-is-folder"
          >
            <el-checkbox
              v-if="showCheckbox"
              v-model="i._checked"
              class="wl-checkbox"
              @change="listItemCheck($event, i)"
            ></el-checkbox>
            <div @click="clickDataFile(i, i[selfIsFolder])">
              <img
                :src="fileTypeIcon(i)"
                class="name-col-icon"
                alt="文件类型图标"
              />
              <p class="list-item-name" :title="i[selfProps.name]">
                {{
                  i.formatter
                    ? i.formatter(i, null, i[selfProps.name], idx)
                    : i[selfProps.name]
                }}
              </p>
            </div>
          </li>
        </ul>
        <!-- 横排型文件列表 -->
        <slot name="main"></slot>
      </div>
    </el-scrollbar>
    <!-- slot 自定义dom区 -->
    <slot></slot>
  </div>
</template>

<script>
import { baseURL } from "@/config/settings";
export default {
  name: "DataSetExplorer",
  components: {},
  props: {
    dataExplorerVisible: {
      type: Boolean,
      default: false,
    },
    // 数据类型
    dataType: {
      type: Number,
      default: 10,
    },
    // 当前路径
    currentPath: {
      type: String,
      default: "",
    },
    // 是否显示表格
    showList: {
      type: Boolean,
      default: false,
    },
    // 文件表格数据
    data: {
      type: Array,
      default() {
        return [];
      },
    },
    // 是否显示复选框
    showCheckbox: {
      type: Boolean,
      default: true,
    },
    // 表格是否显示边框
    showBorder: {
      type: Boolean,
      default: true,
    },
    // 是否显示顺序号
    showIndex: {
      type: Boolean,
      default: true,
    },
    // 文件表头数据
    // 【[参数：所有el-Table-column Attributes] (https://element.eleme.cn/#/zh-CN/component/table)】
    columns: {
      type: Array,
      default() {
        return [];
      },
    },
    // 配置项
    props: {
      type: Object,
      default: () => {
        return {};
      },
    },
    // 校验是否文件夹函数，（row）参数为当前行数据，
    // 用于复杂类型，当isFolderFn优先使用计算结果，不存在时使用props配置内的isFolder字段
    isFolderFn: {
      type: Function,
      default: () => {},
    },
    // 是否锁定文件
    // 文件夹函数,true则不可进行操作
    isLockFn: {
      type: Function,
      default: () => {},
    },
    clickFileType: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {};
  },
  computed: {
    // 自身表头数据
    selfColumns() {
      let _data = this.columns || [];
      _data.forEach((i, idx) => {
        i._id = `_col_${idx}`;
      });
      return _data;
    },
    // 自身配置项
    selfProps() {
      return {
        isFolder: "isFolder", // Boolean 用于有布尔值字段表示数据是否文件夹类型的情况,当使用isFolderFn函数时，此参数会被忽略
        isLock: "isLock", // Boolean 用于有布尔值字段表示数据是否锁定文件类型的情况,当使用isLockFn函数时，此参数被忽略
        name: "file_name", // String 用于显示名称列的字段
        suffix: "suffix", // String 用于判断后缀或显示文件类型列的字段
        match: "file_name", // String 用于设定输入框自动补全的匹配字段
        pathName: "name", // String 路径数据 显示名称字段
        pathId: "id", // String 路径数据 id字段
        pathPid: "pid", // String 路径数据 pid字段
        pathChildren: "children", // String 路径数据 children字段
        pathDisabled: "disabled", // String 路径数据 禁用字段
        pathConnector: "\\", // String 路径父子数据拼接连接符,默认为'\'
        pathParents: "parents", // String 路径数据所有直系祖先节点自增长identityId逗号拼接
        pathIdentityId: "identityId", // String 路径数据自增长id
        ...this.props,
      };
    },
    // 将是否文件夹的两种判断方式合并返回
    selfIsFolder() {
      return this.isFolderFn ? "isFolder" : this.selfProps.isFolder;
    },
    // 将是否锁定文件、文件夹的两种判断方式合并返回
    selfIsLock() {
      return this.isLockFn ? "isLock" : this.selfProps.isLock;
    },
  },
  watch: {
    // 检测data数据更新列表
    data(val, old) {
      this.rowSelection();
    },
    showList(val, old) {
      this.rowSelection();
    },
  },
  created() {},
  mounted() {
    this.$nextTick(function () {
      this.rowSelection();
    });
  },
  methods: {
    // 记录多选列表数据
    filterChecked(val) {
      console.log("filterChecked checked_files", this.dataType, val);
      console.log("===================");
      const selected_data = this.$refs["wl-table"].selection;
      this.$emit("setCheckFiles", selected_data);
    },
    // 根据文件类型显示图标
    fileTypeIcon(row) {
      let _path = "";
      // 文件夹
      if (row[this.selfIsFolder]) {
        _path = row[this.selfIsLock]
          ? require("./images/file_automatic@3x.png")
          : require("./images/folder@3x.png");
        return _path;
      }
      // 其他根据后缀类型
      let _suffix = row[this.selfProps.suffix];
      if (!_suffix) {
        _path = require("./images/file_none@3x.png");
        return _path;
      }
      if (["jpg", "jpeg", "png", "gif", "bmp"].includes(_suffix)) {
        // 图片
        _path = require("./images/file_img@3x.png");
      } else if (["zip", "rar", "7z", "gz", "tar"].includes(_suffix)) {
        _path = require("./images/file_zip@3x.png");
      } else if (
        ["avi", "mp4", "rmvb", "flv", "mov", "m2v", "mkv"].includes(_suffix)
      ) {
        _path = require("./images/file_video@3x.png");
      } else if (["mp3", "wav", "wmv", "wma"].includes(_suffix)) {
        _path = require("./images/file_mp3@3x.png");
      } else if (["xls", "xlsx"].includes(_suffix)) {
        _path = require("./images/file_excel@3x.png");
      } else if (["doc", "docx"].includes(_suffix)) {
        _path = require("./images/file_docx@3x.png");
      } else if ("pdf" === _suffix) {
        _path = require("./images/file_pdf@3x.png");
      } else if ("ppt" === _suffix) {
        _path = require("./images/file_ppt@3x.png");
      } else if ("txt" === _suffix) {
        _path = require("./images/file_txt@3x.png");
      } else {
        _path = require("./images/file_none@3x.png");
      }
      return _path;
    },
    // 点击文件夹/文件, 若为文件夹, 则进入下级, 若为文件, 则提供下载/选择
    async clickDataFile(row, isFolder) {
      console.log("clickDataFile clickFileType", this.clickFileType);
      console.log("clickDataFile isFolder", isFolder);
      console.log(
        "clickDataFile this.clickFileType === 0",
        this.clickFileType === 0
      );
      if (!isFolder) {
        if (this.clickFileType === 0) {
          const file_url = row.file_uri;
          const link = document.createElement("a");
          link.href = `${baseURL}${file_url}`;
          link.target = "_blank";
          document.body.appendChild(link);
          link.click();
          link.remove();
          return true;
        } else {
          row._checked = !row._checked;
          this.$refs["wl-table"].toggleRowSelection(row, row._checked);
          const selected_data = this.$refs["wl-table"].selection;
          this.$emit("setCheckFiles", selected_data);
          return true;
        }
      } else {
        console.log("clickDataFile dataType", this.dataType);
        console.log("clickDataFile relative_path", row.relative_path);
        this.$emit("getFileList", this.dataType, row.relative_path);
      }
    },
    // 列表模式记录多选数据
    listItemCheck(check, val) {
      console.log("listItemCheck", check, val);
      val._checked = check;
      this.$refs["wl-table"].toggleRowSelection(val, val._checked);
      const selected_data = this.$refs["wl-table"].selection;
      this.$emit("setCheckFiles", selected_data);
    },
    rowSelection() {
      const checked = [];
      this.data.forEach((item) => {
        if (item._checked) {
          checked.push(item);
        }
      });
      checked.forEach((item) => {
        this.$nextTick(function () {
          this.$refs["wl-table"].toggleRowSelection(item, true);
        });
      });
      this.$forceUpdate();
    },
    handleDataChange(val) {},
  },
};
</script>

<style lang="scss">
@import "./css/index.css";
@import "./css/clear.css";
@import "./icons/iconfont.css";
</style>
