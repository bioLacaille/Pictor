/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 路由守卫
 **/
import router from "@/router";
import store from "@/store";
import VabProgress from "nprogress";
import "nprogress/nprogress.css";
import { Message } from "element-ui";
import getPageTitle from "@/utils/pageTitle";
import {
  authentication,
  loginInterception,
  routesWhiteList,
  progressBar,
  recordRoute,
  messageDuration,
} from "./settings";

const infoMsg = (message) => {
  return Message({
    message: message,
    type: "warning",
    duration: messageDuration,
  });
};
VabProgress.configure({
  easing: "ease",
  speed: 500,
  trickleSpeed: 200,
  showSpinner: false,
});
router.beforeResolve(async (to, from, next) => {
  console.log("生成路由");
  if (progressBar) VabProgress.start();
  let hasToken = store.getters["user/accessToken"];
  let hasWorkZone = store.getters["workzone/workZone"];
  console.log("hasToken:", hasToken);
  console.log("hasWorkZone:", hasWorkZone);
  if (!loginInterception) hasToken = true;
  if (hasToken) {
    if (hasWorkZone || to.path === "/workzones") {
      if (to.path === "/login") {
        next({ path: "/" });
        if (progressBar) VabProgress.done();
      } else {
        const hasPermissions =
          store.getters["user/permissions"] &&
          store.getters["user/permissions"].length > 0;
        console.log("hasPermissions:", hasPermissions);
        if (hasPermissions) {
          next();
        } else {
          try {
            const permissions = await store.dispatch("user/getInfo");
            console.log("get permissions:", permissions);
            let accessRoutes = [];
            if (authentication === "intelligence") {
              accessRoutes = await store.dispatch(
                "routes/setRoutes",
                permissions
              );
            } else if (authentication === "all") {
              accessRoutes = await store.dispatch("routes/setAllRoutes");
            }
            router.addRoutes(accessRoutes);
            next({ ...to, replace: true });
          } catch {
            await store.dispatch("user/resetAccessToken");
            if (progressBar) VabProgress.done();
          }
        }
      }
    } else {
      infoMsg("你尚未选择工作区, 请先选择工作区！");
      next("/workzones");
    }
  } else {
    if (routesWhiteList.indexOf(to.path) !== -1) {
      next();
    } else {
      if (recordRoute) {
        next(`/login?redirect=${to.path}`);
      } else {
        next("/login");
      }

      if (progressBar) VabProgress.done();
    }
  }
  document.title = getPageTitle(to.meta.title);
});
router.afterEach(() => {
  if (progressBar) VabProgress.done();
});
