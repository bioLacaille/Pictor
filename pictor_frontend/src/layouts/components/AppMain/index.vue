<template>
  <section class="app-main-container">
    <transition mode="out-in" name="fade-transform">
      <keep-alive
        v-if="routerView"
        :include="cachedRoutes"
        :max="keepAliveMaxNum"
      >
        <router-view :key="key" class="app-main-height" />
      </keep-alive>
    </transition>
    <footer v-show="footerCopyright" class="footer-copyright">
      Copyright
      <font-awesome-icon :icon="['fas', 'copyright']" />
      {{ title }} {{ fullYear }} by {{ copyright }}
    </footer>
  </section>
</template>

<script>
/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 布局展示主要内容
 * 在config/setting.js 中配置 copyright, footerCopyright, title 决定示页面底部版权信息
 * keepAliveMaxNum 为 缓存路由的最大数量
 **/
import { mapGetters } from "vuex";
import {
  copyright,
  footerCopyright,
  keepAliveMaxNum,
  title,
} from "@/config/settings";

export default {
  name: "AppMain",
  components: {},
  data() {
    return {
      show: false,
      fullYear: new Date().getFullYear(),
      copyright,
      title,
      keepAliveMaxNum,
      routerView: true,
      footerCopyright,
    };
  },
  computed: {
    ...mapGetters({
      visitedRoutes: "tagsBar/visitedRoutes",
      device: "settings/device",
      skeleton: "settings/skeleton",
    }),
    cachedRoutes() {
      const cachedRoutesArr = [];
      this.visitedRoutes.forEach((item) => {
        if (!item.meta.noKeepAlive) {
          cachedRoutesArr.push(item.name);
          this.handleSkeleton();
        }
      });
      return cachedRoutesArr;
    },
    key() {
      return this.$route.path;
    },
  },
  watch: {
    $route: {
      handler(route) {
        if ("mobile" === this.device) {
          this.$store.dispatch("settings/foldSideBar");
        }
      },
      immediate: true,
    },
  },
  created() {
    //重载所有路由
    this.$baseEventBus.$on("reloadRouterView", () => {
      this.routerView = false;
      this.$nextTick(() => {
        this.routerView = true;
        this.handleSkeleton();
      });
    });
  },
  mounted() {
    this.handleSkeleton();
  },
  methods: {
    handleSkeleton() {
      if (this.skeleton) {
        this.show = true;
        setTimeout(() => {
          this.show = false;
        }, 200);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.app-main-container {
  position: relative;
  width: 100%;
  overflow: hidden;
  .app-main-height {
    min-height: $base-app-main-height;
  }

  .footer-copyright {
    min-height: 55px;
    line-height: 55px;
    color: rgba(0, 0, 0, 0.45);
    text-align: center;
    border-top: 1px dashed $base-border-color;
  }
}
</style>
