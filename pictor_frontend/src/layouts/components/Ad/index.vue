<template>
  <div class="vab-ad">
    <el-carousel
      v-if="adList"
      height="30px"
      direction="vertical"
      :autoplay="true"
      :interval="3000"
      indicator-position="none"
    >
      <el-carousel-item v-for="(item, index) in adList" :key="index">
        <el-tag type="warning">
          当前工作区:{{ workZone.serial_number }}({{ workZone.name }})</el-tag
        >
        <el-tooltip
          v-if="item.content"
          class="item"
          effect="dark"
          :content="item.content"
          placement="top"
        >
          <a v-if="item.link" target="_blank" :href="item.link">
            {{ item.title }}</a
          >
          <span v-else>{{ item.title }}</span>
        </el-tooltip>
        <span v-else>{{ item.title }}</span>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>
<script>
/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 布局中展示公告信息
 * 若存在跳转链接，点击具体公告时将跳转
 **/
import store from "@/store";
import { getAnnouncementList } from "@/api/announcement";
export default {
  data() {
    return {
      workZone: store.getters["workzone/workZone"],
      adList: [],
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      this.listLoading = true;
      const data = await getAnnouncementList({
        not_page: true,
        is_publish: true,
      });
      this.adList = data.results;
      this.all_count = data.all_count;
      setTimeout(() => {
        this.listLoading = false;
      }, 500);
    },
  },
};
</script>
<style lang="scss" scoped>
.vab-ad {
  height: 30px;
  padding-right: $base-padding;
  padding-left: $base-padding;
  line-height: 30px;
  cursor: pointer;
  background: #eef1f6;
  box-shadow: 0 -1px 2px rgba(0, 21, 41, 0.08) inset;

  a {
    color: #999;
  }
}
</style>
