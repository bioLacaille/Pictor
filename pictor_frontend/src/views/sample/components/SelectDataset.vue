<template>
  <el-dialog
    append-to-body
    title="选择关联数据(TODO:增加移除已选项功能)"
    :visible.sync="selectDataDialog"
    width="80%"
    @close="close"
  >
    <div class="personalCenter-container">
      <explorer-table
        ref="wl-explorer-cpt"
        :data-explorer-visible="related_param.dataExplorerVisible"
        :columns="filer_table_columns"
        :data="sample_related_files"
        :props="explorer_prop"
        :show-list="related_param.showList"
        :show-border="related_param.showBorder"
        :show-checkbox="related_param.showCheckbox"
        :show-index="related_param.showIndex"
      >
      </explorer-table>
      <el-divider content-position="left">选择文件</el-divider>
      <dataset
        ref="sample-dataset"
        :data-header-visible="not_related_param.dataHeaderVisible"
        :data-search-visible="not_related_param.dataSearchVisible"
        :data-explorer-visible="not_related_param.dataExplorerVisible"
        :show-list="not_related_param.showList"
        :only-directory="not_related_param.onlyDirectory"
        :only-file="not_related_param.onlyFile"
        :only-show-current="not_related_param.onlyShowCurrent"
        :show-border="not_related_param.showBorder"
        :show-checkbox="not_related_param.showCheckbox"
        :show-index="not_related_param.showIndex"
        :click-file-type="not_related_param.clickFileType"
        :checked-file-call-back="not_related_param.checkedFileCallBack"
        :remember-checked="sample_related_files"
        @getCheckFiles="getCheckFiles"
      ></dataset>
    </div>
    <div slot="footer" class="dialog-footer">
      <el-button @click="close">取 消</el-button>
      <el-button type="primary" @click="save">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { getDataSetType, getDataSetList } from "@/api/dataset";
import Dataset from "@/components/DataSet"; // 导入文件管理器
import ExplorerTable from "@/components/DataSet/Explorer/table"; // 导入文件管理器
import store from "@/store";
import { relatedSampleFiles, getRelatedSampleFiles } from "@/api/sample";
export default {
  name: "SelectDataset",
  components: {
    Dataset,
    ExplorerTable,
  },
  data() {
    const _GB = 1024 * 1024 * 1024; // GB
    const _MB = 1024 * 1024;
    const _KB = 1024; // GB
    return {
      // 自定义表格列
      filer_table_columns: [
        {
          label: "文件名称",
          prop: "file_name",
          minWidth: 120,
        },
        {
          label: "类型",
          align: "center",
          width: 90,
          formatter(row) {
            return row.file_type === 20 ? "文件夹" : row.suffix;
          },
        },
        {
          label: "大小",
          width: 90,
          align: "center",
          formatter(row) {
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
        },
        {
          label: "修改日期",
          align: "center",
          minWidth: 120,
          formatter(row) {
            return row.edit_time.split("T")[0] || "-";
          },
        },
        {
          label: "创建日期",
          align: "center",
          minWidth: 120,
          formatter(row) {
            return row.created_time.split("T")[0] || "-";
          },
        },
        {
          label: "上传人员",
          minWidth: 100,
          align: "center",
          formatter(row) {
            return `${row.creator.username}(${row.creator.nickname})` || "-";
          },
        },
      ],
      // 文件管理器配置项
      explorer_prop: {
        name: "file_name",
        match: "file_name",
        suffix: "suffix",
        pathId: "id",
        pathPid: "serial_number",
        pathName: "file_uri",
        pathChildren: "Children", // String 路径数据 children字段
        pathConnector: "\\", // String 路径父子数据拼接连接符,默认为'\'
        pathParents: "Parents", // String 路径数据所有直系祖先节点自增长identityId逗号拼接
        pathIdentityId: "id", // String 路径数据自增长id
      },
      relatedName: "related",
      related_param: {
        dataExplorerVisible: true, // 是否显示
        showList: true, // 是否以表格形式展示
        showBorder: true, // 表格是否显示边框
        showCheckbox: false, // 是否显示复选框
        showIndex: true, // 是否显示顺序号
        clickFileType: 1, // 点击文件触发形式, 0为点击文件即下载/1为点击文件为选择
      },
      not_related_param: {
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
      selectDataDialog: false,
      sample: null,
      sample_related_files: [], // 样本已关联文件
      tmp_related_records: {}, // 记录已经选数据, 用于刷新时保持已选
    };
  },
  created() {},
  methods: {
    showSelectData(row) {
      this.sample = row;
      this.selectDataDialog = true;
      this.getRelatedFileList();
      this.$nextTick(function () {
        this.$refs["sample-dataset"].resetDataSet();
      });
    },
    close() {
      this.sample = null;
      this.sample_related_files = [];
      this.tmp_related_records = {};
      this.selectDataDialog = false;
    },
    // 获取文件数据
    async getRelatedFileList() {
      this.listLoading = true;
      const data = await getRelatedSampleFiles(this.sample.id);
      this.sample_related_files = data.results;
      data.results.forEach((item) => {
        item._checked = true;
        if (
          this.tmp_related_records.hasOwnProperty(
            `${item.data_type}-${item.directory_path}`
          )
        ) {
          this.tmp_related_records[
            `${item.data_type}-${item.directory_path}`
          ].push(item);
        } else {
          this.tmp_related_records[
            `${item.data_type}-${item.directory_path}`
          ] = [item];
        }
      });
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
    getCheckFiles(selected, old, data_type, current_path) {
      console.log("getCheckFiles", selected);
      console.log(
        "getCheckFiles tmp_related_records",
        this.tmp_related_records
      );
      this.tmp_related_records[`${data_type}-${current_path}`] = selected;
      this.sample_related_files = [];
      for (let key in this.tmp_related_records) {
        if (this.tmp_related_records.hasOwnProperty(key)) {
          this.sample_related_files = this.sample_related_files
            .concat(this.tmp_related_records[key])
            .unique(true);
        }
      }
    },
    async save() {
      const data_id = this.sample_related_files.map((item) => item.id);
      if (data_id.length > 0) {
        const data = await relatedSampleFiles(this.sample.id, {
          data_id: data_id,
        });
        const { messages, results } = data;
        this.$baseMessage(messages, "success");
        this.$emit("fetchData");
        this.close();
      } else {
        this.$baseMessage("请选择文件数据", "error");
        return false;
      }
    },
  },
};
</script>
