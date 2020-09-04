<template>
  <dataset
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
  ></dataset>
</template>

<script>
import Dataset from "@/components/DataSet"; // 导入文件管理器
import store from "@/store";
export default {
  name: "DatasetIndex",
  components: {
    Dataset,
  },
  data() {
    return {
      dataHeaderVisible: true, // 是否显示头部操作栏
      dataSearchVisible: true, // 是否显示搜索框
      dataExplorerVisible: true, // 是否显示搜索框
      showList: false, // 是否以表格形式展示
      onlyDirectory: false, // 是否仅仅展示文件夹
      onlyFile: false, // 是否仅仅展示文件
      onlyShowCurrent: false, // 是否仅展示当前类型的数据
      showBorder: true, // 表格是否显示边框
      showCheckbox: true, // 是否显示复选框
      showIndex: true, // 是否显示顺序号
      clickFileType: 0, // 点击文件触发形式, 0为点击文件即下载/1为点击文件为选择
    };
  },
  created() {
    // store.dispatch("uploader/setCurrentTab", 10);
    // store.dispatch("uploader/setDataType", 10);
    // store.dispatch("uploader/setCurrentPath", "");
  },
  methods: {},
};
</script>
