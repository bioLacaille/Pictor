<template>
  <div :class="'logo-container-' + layout">
    <router-link to="/">
      <span
        class="title"
        :class="{ 'hidden-xs-only': layout === 'horizontal' }"
        :title="title"
      >
        {{ title }}
      </span>
    </router-link>
  </div>
</template>
<script>
/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 导航栏 上方 展示LOGO 效果, 当前仅展示缩写， 自行定义
 **/
import { mapGetters } from "vuex";
import { abbreviation } from "@/config/settings";

export default {
  name: "Logo",
  data() {
    return {
      title: abbreviation,
    };
  },
  computed: {
    ...mapGetters({
      logo: "settings/logo",
      layout: "settings/layout",
    }),
  },
};
</script>
<style lang="scss" scoped>
@mixin container {
  position: relative;
  height: $base-top-bar-height;
  overflow: hidden;
  line-height: $base-top-bar-height;
  background: $base-menu-background;
}

@mixin logo {
  display: inline-block;
  width: 32px;
  height: 32px;
  margin-right: 5px;
  color: $base-title-color;
  vertical-align: middle;
}

@mixin title {
  display: inline-block;
  overflow: hidden;
  font-size: 20px;
  font-weight: 600;
  line-height: 55px;
  color: $base-title-color;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: middle;
}

.logo-container-horizontal {
  @include container;

  .logo {
    @include logo;
  }

  .title {
    @include title;
  }
}

.logo-container-vertical {
  @include container;

  height: $base-logo-height;
  line-height: $base-logo-height;
  text-align: center;

  .logo {
    @include logo;
  }

  .title {
    @include title;

    max-width: calc(#{$base-left-menu-width} - 60px);
  }
}
</style>
