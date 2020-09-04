<template>
  <div class="table-container">
    <vab-query-form>
      <vab-query-form-left-panel>
        <el-button icon="el-icon-plus" type="primary" @click="handleAdd"
          >添加
        </el-button>
        <el-button icon="el-icon-delete" type="danger" @click="handleDelete"
          >删除
        </el-button>
      </vab-query-form-left-panel>
      <vab-query-form-right-panel>
        <el-form
          ref="form"
          :model="query_form"
          :inline="true"
          @submit.native.prevent
        >
          <el-form-item>
            <el-input v-model="query_form.search" placeholder="标题" />
          </el-form-item>
          <el-form-item>
            <el-button
              icon="el-icon-search"
              type="primary"
              native-type="submit"
              @click="handleQuery"
              >查询
            </el-button>
          </el-form-item>
        </el-form>
      </vab-query-form-right-panel>
    </vab-query-form>

    <el-table
      ref="notificationRuleTable"
      v-loading="listLoading"
      :data="list"
      :element-loading-text="elementLoadingText"
      @selection-change="setSelectRows"
      @sort-change="tableSortChange"
    >
      <el-table-column
        show-overflow-tooltip
        type="selection"
        width="55"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="是否发布"
        prop="is_publish"
        sortable="custom"
        width="120"
      >
        <template slot-scope="scope">
          <el-tag :type="isActiveStatusFilter(scope.row.is_publish)">{{
            isActiveFilter(scope.row.is_publish)
          }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="公告标题"
        prop="title"
        min-width="200"
        sortable="custom"
      >
      </el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="创建日期"
        prop="created_time"
        width="200"
        sortable="custom"
      ></el-table-column>
      <el-table-column
        show-overflow-tooltip
        label="操作"
        width="180px"
        fixed="right"
      >
        <template slot-scope="scope">
          <el-button type="text" @click="handleEdit(scope.row)"
            >编辑
          </el-button>
          <el-button type="text" @click="handleDelete(scope.row)"
            >删除
          </el-button>
          <el-button
            v-if="scope.row.is_publish"
            type="text"
            @click="handlePublish(scope.row, false)"
            >下架
          </el-button>
          <el-button v-else type="text" @click="handlePublish(scope.row, true)"
            >发布
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      :background="background"
      :current-page="query_form.page"
      :layout="layout"
      :page-size="query_form.page_size"
      :total="all_count"
      @current-change="handleCurrentChange"
      @size-change="handleSizeChange"
    ></el-pagination>
    <announcement-edit
      ref="announcement-edit"
      @fetchData="fetchData"
    ></announcement-edit>
  </div>
</template>

<script>
import AnnouncementEdit from "./components/AnnouncementEdit";
import {
  getAnnouncementList,
  deleteAnnouncement,
  bulkDeleteAnnouncement,
  publishAnnouncement,
} from "@/api/announcement";
export default {
  name: "NotificationRuleTable",
  components: {
    AnnouncementEdit,
  },
  data() {
    return {
      listLoading: true,
      background: true,
      layout: "total, sizes, prev, pager, next, jumper",
      elementLoadingText: "正在加载...",
      list: [],
      all_count: 0,
      select_rows: "",
      query_form: {
        page: 1,
        page_size: 10,
        search: "",
        ordering: null,
      },
    };
  },
  created() {
    this.fetchData();
  },
  beforeDestroy() {},
  mounted() {},
  methods: {
    isActiveFilter(is_active) {
      if (is_active === true) {
        return "是";
      } else {
        return "否";
      }
    },
    isActiveStatusFilter(is_active) {
      if (is_active === true) {
        return "success";
      } else {
        return "danger";
      }
    },
    tableSortChange(data) {
      const { prop, order } = data;
      if (order === "ascending" || order === null) {
        this.query_form.ordering = prop;
      } else {
        this.query_form.ordering = `-${prop}`;
      }
      this.fetchData();
    },
    setSelectRows(val) {
      this.select_rows = val;
    },
    handleAdd() {
      this.$refs["announcement-edit"].showEdit();
    },
    handleEdit(row) {
      this.$refs["announcement-edit"].showEdit(row);
    },
    handleDelete(row) {
      if (row.id) {
        this.$baseConfirm("你确定要删除当前项吗", null, async () => {
          const data = await deleteAnnouncement(row.id);
          const messages = data.messages;
          this.$baseMessage(messages, "success");
          this.fetchData();
        });
      } else {
        if (this.select_rows.length > 0) {
          const ids = this.select_rows.map((item) => item.id);
          this.$baseConfirm("你确定要删除选中项吗", null, async () => {
            const data = await bulkDeleteAnnouncement({
              deleted_objects: ids,
            });
            const messages = data.messages;
            this.$baseMessage(messages, "success");
            this.fetchData();
          });
        } else {
          this.$baseMessage("未选中任何行", "error");
          return false;
        }
      }
    },
    handlePublish(row, publish = true) {
      let msg = "发布";
      if (!publish) {
        msg = "下架";
      }
      this.$baseConfirm(`你确定要${msg}前项吗`, null, async () => {
        const data = await publishAnnouncement(row.id, {
          publish: publish,
        });
        const messages = data.messages;
        this.$baseMessage(messages, "success");
        this.fetchData();
      });
    },
    handleSizeChange(val) {
      this.query_form.page_size = val;
      this.fetchData();
    },
    handleCurrentChange(val) {
      this.query_form.page = val;
      this.fetchData();
    },
    handleQuery() {
      this.query_form.page = 1;
      this.fetchData();
    },
    async fetchData() {
      this.listLoading = true;
      const data = await getAnnouncementList(this.query_form);
      this.list = data.results;
      this.all_count = data.all_count;
      setTimeout(() => {
        this.listLoading = false;
      }, 500);
    },
  },
};
</script>
