<template>
  <div class="dk-page-header">
    <el-breadcrumb separator="/">
      <template v-for="(item, index) in breadcrumb">
        <el-breadcrumb-item
          v-if="item.name || item.path"
          :key="index"
          :to="item"
          >{{ item.title }}</el-breadcrumb-item
        >
        <el-breadcrumb-item v-else-if="item.href" :key="index"
          ><a :href="item.href" :target="item.target ? item.target : 'self'">{{
            item.title
          }}</a></el-breadcrumb-item
        >
        <el-breadcrumb-item v-else :key="index">{{
          item.title
        }}</el-breadcrumb-item>
      </template>
    </el-breadcrumb>
    <div v-if="title || description" class="dk-page-header-title">
      <h2>{{ title }}</h2>
      <template v-if="backButton !== 'none'">
        <el-divider direction="vertical"></el-divider>
        <el-button type="text" class="dk-page-header-back" @click="goBack"
          >返回<i class="el-icon-right"></i
        ></el-button>
      </template>
      <div
        v-if="description"
        class="dk-page-header-title-desc"
        v-html="description"
      ></div>
    </div>
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "DkPageHeader",
  props: {
    // eslint-disable-next-line vue/require-default-prop
    title: String,
    // eslint-disable-next-line vue/require-default-prop
    description: String,
    breadcrumb: {
      type: Array,
      default() {
        return [];
      },
    },
    backButton: {
      type: String,
      default: "none", // 可选的值 none|back|event
    },
  },
  methods: {
    goBack() {
      if (this.backButton === "back") {
        this.$router.back();
      } else if (this.backButton === "event") {
        this.$emit("back");
      }
    },
  },
};
</script>

<style scoped></style>
