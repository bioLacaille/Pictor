<template>
  <el-form
    :inline="true"
    :size="size"
    :model="file"
    class="wl-header-file"
    @submit.native.prevent
  >
    <el-form-item class="file-path-box">
      <div
        v-show="!layout.edit_path"
        class="file-path-text"
        :class="{ small: size === 'small' }"
        @click="handleFilePath"
      >
        <img
          class="file-path-img"
          src="../images/folder@3x.png"
          alt="文件夹"
          title="文件夹"
        />
        {{ file.path }}
      </div>
      <el-autocomplete
        v-if="layout.edit_path"
        ref="file-path-ipt"
        v-model="file.path"
        class="u-full"
        placeholder="请输入文件路径"
        :fetch-suggestions="pathQuerySearch"
        @keyup.enter.native="filePathChange"
        @select="filePathChange"
      >
        <img
          slot="prefix"
          class="file-path-img"
          src="../images/folder@3x.png"
          alt="文件夹"
          title="文件夹"
        />
      </el-autocomplete>
    </el-form-item>
    <el-form-item class="file-search-box">
      <el-input
        v-model="file.key"
        placeholder="请输入关键字搜索"
        @keyup.enter.native="fileSearch()"
      >
        <el-button
          slot="append"
          icon="el-icon-search file-search"
          @click="fileSearch()"
        ></el-button>
      </el-input>
    </el-form-item>
    <el-form-item class="file-handle-box">
      <i
        class="iconfont icon-wl-left file-path-handle"
        :class="{ 'u-disabled': pathIsStart }"
        @click="pathBtn('prv')"
      ></i>
      <i
        class="iconfont icon-wl-right file-path-handle"
        :class="{ 'u-disabled': pathIsEnd }"
        @click="pathBtn('next')"
      ></i>
      <i
        class="iconfont icon-wl-up file-path-handle"
        :class="{ 'u-disabled': path.level === 1 }"
        @click="pathBtn('top')"
      ></i>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  name: "FilePath",
};
</script>
