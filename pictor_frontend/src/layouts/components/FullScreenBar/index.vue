<template>
  <span :title="isFullscreen ? '退出全屏' : '进入全屏'">
    <font-awesome-icon
      :icon="[
        'fas',
        isFullscreen ? 'compress-arrows-alt' : 'expand-arrows-alt',
      ]"
      @click="click"
    ></font-awesome-icon>
  </span>
</template>

<script>
/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 是否全屏按钮
 **/
import screenfull from "screenfull";

export default {
  name: "FullScreenBar",
  data() {
    return {
      isFullscreen: false,
    };
  },
  mounted() {
    this.init();
  },
  beforeDestroy() {
    this.destroy();
  },
  methods: {
    click() {
      if (!screenfull.isEnabled) {
        this.$baseMessage("开启全屏失败", "error");
        return false;
      }
      screenfull.toggle();
      this.$emit("refresh");
    },
    change() {
      this.isFullscreen = screenfull.isFullscreen;
    },
    init() {
      if (screenfull.isEnabled) {
        screenfull.on("change", this.change);
      }
    },
    destroy() {
      if (screenfull.isEnabled) {
        screenfull.off("change", this.change);
      }
    },
  },
};
</script>
