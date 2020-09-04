<template>
  <div class="personalCenter-container">
    <el-tabs v-model="currentTab" tab-position="left" @tab-click="changeTab">
      <el-tab-pane
        v-for="item in data_types"
        :key="item.key"
        :name="item.value"
        :label="item.value"
      >
        <!-- 头部按钮区 -->
        <data-header
          :data-header-visible="dataHeaderVisible"
          :data-type="current_data_type"
          :current-path="current_path"
          :show-list="show_list"
          :checked-files="checked_files"
          @getFileList="getFileList"
          @setDataCurrentPath="setDataCurrentPath"
          @setDataCurrentType="setDataCurrentType"
          @changeShowList="changeShowList"
        ></data-header>
        <data-search
          size="medium"
          :data-search-visible="dataSearchVisible"
          :data-type="current_data_type"
          :current-path="current_path"
          :show-list="show_list"
          :checked-files="checked_files"
          @getFileList="getFileList"
          @setDataCurrentPath="setDataCurrentPath"
          @setDataCurrentType="setDataCurrentType"
        ></data-search>
        <!-- 文件列表 -->
        <wlExplorer
          ref="wl-explorer-cpt"
          :data-type="current_data_type"
          :current-path="current_path"
          :columns="filer_table_columns"
          :is-folder-fn="isFolderFn"
          :data="filer_table_data"
          :props="explorer_prop"
          :show-list="show_list"
          @getFileList="getFileList"
          @setCheckFiles="setCheckFiles"
        >
        </wlExplorer>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { getDataSetType, getDataSetList } from "@/api/dataset";
import WlExplorer from "@/components/DataSet/Explorer"; // 导入文件管理器
import DataHeader from "@/components/DataSet/DataHeader";
import DataSearch from "@/components/DataSet/DataSearch";
import store from "@/store";
export default {
  name: "Dataset",
  components: {
    DataHeader,
    DataSearch,
    WlExplorer,
  },
  data() {
    const _GB = 1024 * 1024 * 1024; // GB
    const _MB = 1024 * 1024;
    const _KB = 1024; // GB
    return {
      dataHeaderVisible: true, // 是否显示头部操作栏
      dataSearchVisible: true, // 是否显示搜索框
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
          minWidth: 90,
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
          width: 120,
          formatter(row) {
            return row.edit_time.split("T")[0] || "-";
          },
        },
        {
          label: "创建日期",
          align: "center",
          width: 120,
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
      currentTab: "", // 当前tab
      data_types: [], // 所有数据分类
      current_data_type: 10, // 当前数据分类
      current_path: "", // 当前路径
      show_list: false, // 是否以表格形式展示
      filer_table_data: [], // 表格数据
      checked_files: [], // 已选文件
    };
  },
  created() {
    this.getDataTypes();
    this.getFileList();
  },
  methods: {
    setDataCurrentPath(current_path) {
      this.current_path = current_path;
    },
    setDataCurrentType(data_type) {
      this.current_data_type = data_type;
    },
    setCheckFiles(files) {
      let selected = [];
      files.forEach((item) => {
        selected.push(item.id);
      });
      this.filer_table_data.forEach(
        (i) => (i._checked = selected.includes(i.id))
      );
      this.checked_files = files;
    },
    // 获取所有分类
    async getDataTypes() {
      const data = await getDataSetType();
      this.data_types = data.results;
      // 获取当前所在分类
      const currentTab_key = store.getters["uploader/currentTab"];
      if (!currentTab_key) {
        this.current_data_type = this.data_types[0].key;
        this.currentTab = this.data_types[0].value;
      } else {
        for (let i = 0; i < this.data_types.length; i++) {
          if (currentTab_key === this.data_types[i].key) {
            this.current_data_type = this.data_types[i].key;
            this.currentTab = this.data_types[i].value;
          }
        }
      }
    },
    // 获取文件数据
    async getFileList(data_type, current_path = null, search = "") {
      this.listLoading = true;
      if (!data_type) {
        const currentTab_key = store.getters["uploader/dataType"];
        if (currentTab_key) {
          data_type = currentTab_key;
        } else {
          data_type = this.current_data_type;
        }
      }
      if (current_path === null) {
        current_path = this.current_path;
      }
      const data = await getDataSetList({
        not_page: true,
        data_type: data_type,
        current_path: current_path,
        search: search,
      });
      this.setDataCurrentType(data_type);
      this.setDataCurrentPath(current_path);
      data.results.forEach((i) => (i._checked = false));
      this.filer_table_data = data.results;
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
    // 自定义如何判断是否文件夹
    isFolderFn(row) {
      return row.file_type === 20;
    },
    // 更换展示形式
    changeShowList(show_list = false) {
      this.show_list = show_list;
    },
    // 更改当前tab类型
    changeTab(obj, e) {
      this.current_data_type = obj.$vnode.key;
      this.current_path = "";
      store.dispatch("uploader/setCurrentTab", obj.$vnode.key);
      store.dispatch("uploader/setDataType", obj.$vnode.key);
      store.dispatch("uploader/setCurrentPath", this.current_path);
      this.getFileList();
    },
  },
};
</script>
