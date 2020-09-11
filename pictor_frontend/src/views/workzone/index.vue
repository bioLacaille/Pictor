<template>
  <div class="card-container">
    <div style="text-align: center">
      <vab-colorful-icon style="font-size: 150px" icon-class="pictor" />
      <h1 style="font-size: 30px">Pictor-Biological-Analysis-Platform</h1>
    </div>
    <br />
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
        <el-divider content-position="left"
          >工作区----请先选择或创建你的工作区, 并将相关用户添加进该工作区,
          工作区内成员将共享该工作区数据</el-divider
        >
        <div style="float: right; display: flex; margin-left: 10px">
          <el-radio-group
            v-if="is_admin"
            v-model="queryForm.show_all"
            style="padding-left: 10px"
            @change="handleChangeShow"
          >
            <el-radio-button :key="true" :label="true">全 部</el-radio-button>
            <el-radio-button :key="false" :label="false"
              >与自己相关</el-radio-button
            >
          </el-radio-group>
          <el-form
            ref="form"
            style="padding-left: 20px"
            :model="queryForm"
            :inline="true"
            @submit.native.prevent
          >
            <el-form-item>
              <el-input
                v-model="queryForm.search"
                placeholder="工作区编号/工作区名称"
              />
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
        </div>
      </el-col>
      <el-col :xs="24" :sm="8" :md="8" :lg="8" :xl="6">
        <el-card shadow="hover" style="text-align: center; height: 380px">
          <div
            tabindex="0"
            class="el-upload el-upload--picture-card"
            style="margin-top: 100px"
            @click="handleAdd"
          >
            <i data-v-7340870a="" class="el-icon-plus"></i
            ><input type="file" name="file" class="el-upload__input" />
          </div>
        </el-card>
      </el-col>
      <el-col
        v-for="(item, index) in list"
        :key="index"
        :xs="24"
        :sm="8"
        :md="8"
        :lg="8"
        :xl="6"
      >
        <el-card shadow="hover" style="height: 380px">
          <div
            slot="header"
            style="text-align: center; cursor: pointer"
            @click="handleSelect(item)"
          >
            <h1 style="font-size: 30px">{{ item.serial_number }}</h1>
            <p>{{ item.name }}</p>
          </div>
          <div
            style="text-align: center; cursor: pointer"
            @click="handleSelect(item)"
          >
            <font-awesome-layers full-width class="fa-4x">
              <font-awesome-icon
                icon="star"
                :style="{ color: '#ADD8E6' }"
                size="lg"
              />
              <font-awesome-layers-text
                transform="down-0 right-1 shrink-12"
                :value="item.name.slice(0, 1)"
                style="color: black; font-size: 3em; text-align: center"
              />
            </font-awesome-layers>
            <br />
            <br />
            <div class="tip">
              <el-alert type="info" :closable="false" center>
                <p
                  style="
                    overflow: hidden;
                    -webkit-line-clamp: 2;
                    text-overflow: ellipsis;
                    display: -webkit-box;
                    -webkit-box-orient: vertical;
                  "
                >
                  {{ item.remark }}
                </p>
              </el-alert>
            </div>
          </div>
          <br />
          <el-divider>{{ item.created_time }}</el-divider>
          <div style="text-align: center">
            <el-button type="primary" plain @click="handleSelect(item)"
              >进入</el-button
            >
            <el-button
              v-if="item.permissions.edit"
              type="success"
              plain
              @click="handleEdit(item)"
              >编辑</el-button
            >
            <el-button
              v-if="item.permissions.change_member"
              type="info"
              plain
              @click="handleSelectUser(item)"
              >成员</el-button
            >
            <el-button
              v-if="item.permissions.delete"
              type="danger"
              plain
              @click="handleDelete(item)"
              >删除</el-button
            >
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-pagination
      :background="background"
      :current-page="queryForm.page"
      :layout="layout"
      :page-size="queryForm.page_size"
      :total="all_count"
      @current-change="handleCurrentChange"
      @size-change="handleSizeChange"
    ></el-pagination>
    <work-zone-edit ref="edit" @listEvent="fetchData"></work-zone-edit>
    <select-user ref="user"></select-user>
  </div>
</template>

<script>
import { getWorkZoneList, deleteWorkZone } from "@/api/workzone";
import WorkZoneEdit from "./components/WorkZoneEdit";
import SelectUser from "./components/SelectUser";
import store from "@/store";
import router from "@/router";

export default {
  name: "WorkZone",
  components: {
    WorkZoneEdit,
    SelectUser,
  },
  data() {
    return {
      list: null,
      listLoading: true,
      layout: "total, sizes, prev, pager, next, jumper",
      all_count: 0,
      queryForm: {
        show_all: false,
        search: "",
        page: 1,
        page_size: 10,
      },
      background: true,
      dialogFormVisible: false,
      is_admin: false,
    };
  },
  created() {
    const permissions = store.getters["user/permissions"];
    if (permissions.includes("admin") || permissions.includes("super_admin")) {
      this.is_admin = true;
    }
    console.log("is_admin", this.is_admin);
    this.fetchData();
  },
  methods: {
    handleAdd() {
      this.$refs["edit"].showEdit();
    },
    handleEdit(row) {
      this.$refs["edit"].showEdit(row);
    },
    handleSelectUser(row) {
      this.$refs["user"].showSelectUser(row);
    },
    handleSelect(row) {
      store.dispatch("workzone/setWorkZone", row);
      this.$baseNotify(`您已选择工作区: ${row.serial_number}`, `${row.name}`);
      router.push({
        path: "/index",
      });
    },
    handleSizeChange(val) {
      this.page_size = val;
      this.fetchData();
    },
    handleCurrentChange(val) {
      this.page = val;
      this.fetchData();
    },
    handleDelete(row) {
      this.$baseConfirm(
        "删除工作区将导致其关联数据失去关联",
        "你确定要删除该工作区吗?",
        async () => {
          const data = await deleteWorkZone(row.id);
          const messages = data.messages;
          this.$baseMessage(messages, "success");
          this.fetchData();
        }
      );
    },
    handleQuery() {
      this.queryForm.page = 1;
      this.fetchData();
    },
    handleChangeShow(val) {
      this.queryForm.show_all = val;
      this.fetchData();
    },
    async fetchData() {
      this.listLoading = true;
      const data = await getWorkZoneList(this.queryForm);
      this.list = data.results;
      this.all_count = data.all_count;
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
  },
};
</script>
