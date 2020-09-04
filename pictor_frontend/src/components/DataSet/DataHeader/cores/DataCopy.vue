<template>
  <el-dialog
    title="请选择复制目录"
    :visible.sync="dataCopyVisible"
    width="800px"
    @close="close"
  >
    <copy-data-set
      :data-header-visible="dataHeaderVisible"
      :data-search-visible="dataSearchVisible"
      :data-explorer-visible="dataExplorerVisible"
      :show-list="showList"
      :only-directory="onlyDirectory"
      :only-file="onlyFile"
      :only-show-current="onlyShowCurrent"
      :show-border="showBorder"
      :show-checkbox="showCheckbox"
      :show-index="showIndex"
      :click-file-type="clickFileType"
    ></copy-data-set>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">取 消</el-button>
      <el-button type="primary" @click="save">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script>
import Dataset from "@/components/DataSet"; // 导入文件管理器
import store from "@/store";
import { copyMoveDataSet } from "@/api/dataset";
export default {
  name: "DataCopy",
  components: {
    copyDataSet: Dataset,
  },
  props: {},
  data() {
    return {
      dataHeaderVisible: false, // 是否显示头部操作栏
      dataSearchVisible: true, // 是否显示搜索框
      dataExplorerVisible: true, // 是否显示搜索框
      showList: false, // 是否以表格形式展示
      onlyDirectory: true, // 是否仅仅展示文件夹
      onlyFile: false, // 是否仅仅展示文件
      onlyShowCurrent: false, // 是否仅展示当前类型的数据
      showBorder: true, // 表格是否显示边框
      showCheckbox: true, // 是否显示复选框
      showIndex: true, // 是否显示顺序号
      clickFileType: 0, // 点击文件触发形式, 0为点击文件即下载/1为点击文件为选择
      dataCopyVisible: false,
      target_path: "", // 目标路径
    };
  },
  created() {},
  methods: {
    showEdit(selected) {
      this.dataCopyVisible = true;
    },
    close() {
      this.target_path = "";
      this.dataCopyVisible = false;
    },
    save() {
      const _that = this;
    },
  },
};
</script>
