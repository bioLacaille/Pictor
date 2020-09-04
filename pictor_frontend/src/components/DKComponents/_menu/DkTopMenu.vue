<template>
  <el-header class="dk-header-wrapper">
    <div class="dk-header">
      <el-button
        v-if="
          layout === 'aside' ||
          (layout === 'top' && (screen === 'xs' || screen === 'sm'))
        "
        :icon="asideIsOpened ? 'el-icon-s-fold' : 'el-icon-s-unfold'"
        @click="closeAside(!asideIsOpened)"
      ></el-button>
      <div class="dk-header-right">
        <div
          :class="[
            'dk-header-search',
            searchIsOpened ? 'dk-header-search-opened' : '',
          ]"
        >
          <el-button
            icon="ion-md-search"
            @click="headerSearchHandle(!searchIsOpened)"
          ></el-button>
          <el-autocomplete
            ref="header-search"
            v-model="searchValue"
            class="inline-input"
            size="small"
            popper-class="search-popper"
            type="search"
            :fetch-suggestions="searchAutocompleteQuery"
            placeholder="站内搜索"
            :select-when-unmatched="true"
            @select="searchAutocompleteHandle"
            @blur="headerSearchHandle(false)"
          ></el-autocomplete>
        </div>
        <el-tooltip
          class="item"
          effect="dark"
          content="使用文档"
          placement="bottom"
        >
          <el-button icon="ion-md-help-circle-outline"></el-button>
        </el-tooltip>
        <el-button class="dk-header-btn-notifications" size="small">
          <el-badge :value="11" class="item">
            <i class="el-icon-bell"></i>
          </el-badge>
        </el-button>
        <el-dropdown class="dk-header-user">
          <el-button>
            <el-avatar src="/img/avatar.jpg" :size="24"></el-avatar>
            Yanjun
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item icon="el-icon-user">个人中心</el-dropdown-item>
            <el-dropdown-item icon="el-icon-setting">个人设置</el-dropdown-item>
            <el-dropdown-item icon="ion-md-log-out" divided
              >退出登录</el-dropdown-item
            >
          </el-dropdown-menu>
        </el-dropdown>
        <el-dropdown>
          <el-button icon="ion-ios-globe"></el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item class="active">CN 中文站点</el-dropdown-item>
            <el-dropdown-item>EN 英文站点</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
  </el-header>
</template>

<script>
export default {
  name: "DkTopMenu",
  props: {
    value: {
      type: Boolean,
      default: true,
    },
    // eslint-disable-next-line vue/require-default-prop
    screen: String,
  },
  data() {
    return {
      layout: process.env.VUE_APP_LAYOUT,

      asideIsOpened: this.value,

      // 搜索
      searchIsOpened: false,
      searchValue: "",
    };
  },
  watch: {
    value: function (newVal) {
      this.asideIsOpened = newVal;
    },
    asideIsOpened: function () {
      this.$emit("input", this.asideIsOpened);
    },
  },
  methods: {
    /**
     * 搜索
     * @param queryString
     * @param cb
     */
    searchAutocompleteQuery(queryString, cb) {
      // 自动完成
      let results = !queryString
        ? []
        : [
            { value: queryString },
            { value: queryString + queryString },
            { value: queryString + queryString + queryString + queryString },
          ];
      cb(results);
    },
    searchAutocompleteHandle() {
      if (!this.searchValue) return;
      this.$message.info(`您搜索的是“${this.searchValue}”。`);
      this.headerSearchHandle(false);
    },
    headerSearchHandle(isOpen) {
      this.searchIsOpened = isOpen;
      if (isOpen) {
        this.$refs["header-search"].focus();
      } else {
        this.searchValue = "";
      }
    },
    /**
     * 侧边栏展开收起
     */
    closeAside(isOpened) {
      this.asideIsOpened = isOpened;
      this.$emit("aside-collapse", isOpened);
    },
  },
};
</script>

<style scoped></style>
