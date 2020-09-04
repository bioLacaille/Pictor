<template>
  <el-dialog
    append-to-body
    title="选择数据"
    :visible.sync="selectDataDialog"
    width="80%"
    @close="close"
  >
    <dataset
      ref="analysis-dataset"
      :data-header-visible="dataset_param.dataHeaderVisible"
      :data-search-visible="dataset_param.dataSearchVisible"
      :data-explorer-visible="dataset_param.dataExplorerVisible"
      :show-list="dataset_param.showList"
      :only-directory="dataset_param.onlyDirectory"
      :only-file="dataset_param.onlyFile"
      :only-show-current="dataset_param.onlyShowCurrent"
      :show-border="dataset_param.showBorder"
      :show-checkbox="dataset_param.showCheckbox"
      :show-index="dataset_param.showIndex"
      :click-file-type="dataset_param.clickFileType"
      :checked-file-call-back="dataset_param.checkedFileCallBack"
      :remember-checked="selected"
      @getCheckFiles="getCheckFiles"
    ></dataset>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">取 消</el-button>
      <el-button type="primary" @click="saveSelectData">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script>
import Dataset from "@/components/DataSet"; // 导入文件管理器
export default {
  name: "SelectDataset",
  components: {
    Dataset,
  },
  data() {
    const _GB = 1024 * 1024 * 1024; // GB
    const _MB = 1024 * 1024;
    const _KB = 1024; // GB
    return {
      dataset_param: {
        dataHeaderVisible: false, // 是否显示头部操作栏
        dataSearchVisible: true, // 是否显示搜索框
        dataExplorerVisible: true, // 是否显示搜索框
        showList: false, // 是否以表格形式展示
        onlyDirectory: false, // 是否仅仅展示文件夹
        onlyFile: false, // 是否仅仅展示文件
        onlyShowCurrent: false, // 是否仅展示当前类型的数据
        showBorder: true, // 表格是否显示边框
        showCheckbox: true, // 是否显示复选框
        showIndex: true, // 是否显示顺序号
        clickFileType: 1, // 点击文件触发形式, 0为点击文件即下载/1为点击文件为选择
        checkedFileCallBack: true, // 是否返回已选文件
      },
      parameter_index: null,
      selectDataDialog: false,
      selected: [],
      tmp_selected: [],
      selectedFilesPath: [],
    };
  },
  created() {},
  methods: {
    showSelectData(parameter_index) {
      this.selectDataDialog = true;
      this.parameter_index = parameter_index;
      this.$nextTick(function () {
        this.$refs["analysis-dataset"].resetDataSet();
      });
    },
    close() {
      this.selectDataDialog = false;
      this.parameter_index = null;
      this.selected = [];
      this.tmp_selected = [];
      this.selectedFilesPath = [];
    },
    getCheckFiles(selected, old, data_type, current_path) {
      this.tmp_selected[`${data_type}-${current_path}`] = selected;
      this.selected = [];
      for (let key in this.tmp_selected) {
        if (this.tmp_selected.hasOwnProperty(key)) {
          this.selected = this.selected
            .concat(this.tmp_selected[key])
            .unique(true);
        }
      }
    },
    saveSelectData() {
      for (let i = 0; i < this.selected.length; i++) {
        this.selectedFilesPath.push(this.selected[i].file_uri);
      }
      this.$emit(
        "setParameterValue",
        this.parameter_index,
        this.selectedFilesPath.join(",")
      );
      this.close();
    },
  },
};
</script>
