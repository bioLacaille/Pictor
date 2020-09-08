/**
 * @description router全局配置，
 * 其中asyncRoutes只有在intelligence模式下才会用到
 */

import Vue from "vue";
import VueRouter from "vue-router";
import Layout from "@/layouts";
import EmptyLayout from "@/layouts/EmptyLayout";
import { routerMode } from "@/config/settings";

Vue.use(VueRouter);
export const constantRoutes = [
  {
    path: "/login",
    component: () => import("@/views/login/index"),
    hidden: true,
  },
  {
    path: "/401",
    name: "401",
    component: () => import("@/views/401"),
    hidden: true,
  },
  {
    path: "/404",
    name: "404",
    component: () => import("@/views/404"),
    hidden: true,
  },
];

export const asyncRoutes = [
  {
    path: "/workzones",
    name: "workzones",
    component: () => import("@/views/workzone/index"),
    hidden: true,
    meta: {
      title: "工作区",
      icon: "network-wired",
      affix: true,
    },
  },
  {
    path: "/",
    component: Layout,
    redirect: "index",
    children: [
      {
        path: "index",
        name: "index",
        component: () => import("@/views/index/index"),
        meta: {
          title: "首页",
          icon: "home",
          affix: true,
        },
      },
    ],
  },
  {
    path: "/charts",
    component: Layout,
    redirect: "charts",
    children: [
      {
        path: "",
        name: "charts",
        component: () => import("@/views/charts/index"),
        meta: {
          title: "统计图表",
          icon: "chart-pie",
          permissions: ["admin", "super_admin"],
          badge: "Pro",
        },
      },
    ],
  },
  {
    path: "/monitor",
    component: Layout,
    redirect: "monitor",
    children: [
      {
        path: "",
        name: "monitor",
        component: () => import("@/views/monitor/index"),
        meta: {
          title: "实时监控",
          icon: "archive",
          permissions: ["admin", "super_admin"],
          badge: "Pro",
        },
      },
    ],
  },
  {
    path: "/project",
    component: Layout,
    redirect: "project",
    children: [
      {
        path: "",
        name: "project",
        component: () => import("@/views/project/index"),
        meta: {
          title: "项目",
          icon: "weight-hanging",
        },
      },
    ],
  },
  {
    path: "/sample",
    component: Layout,
    redirect: "sample",
    children: [
      {
        path: "",
        name: "sample",
        component: () => import("@/views/sample/index"),
        meta: {
          title: "样本",
          icon: "align-justify",
        },
      },
    ],
  },
  {
    path: "/dataset",
    component: Layout,
    redirect: "dataset",
    children: [
      {
        path: "",
        name: "dataset",
        component: () => import("@/views/dataset/index"),
        meta: {
          title: "数据",
          icon: "database",
        },
      },
    ],
  },
  {
    path: "/analysis",
    component: Layout,
    redirect: "analysis",
    children: [
      {
        path: "analysis",
        name: "analysis",
        component: () => import("@/views/analysis/index"),
        meta: {
          title: "分析任务",
          icon: "tasks",
        },
      },
    ],
  },
  {
    path: "/setting",
    component: Layout,
    redirect: "noRedirect",
    name: "setting",
    meta: {
      title: "设置",
      icon: "wallet",
      permissions: ["super_user", "admin", "super_admin"],
    },
    children: [
      {
        path: "uploadSetting",
        name: "uploadSetting",
        icon: "wallet",
        component: () => import("@/views/serialNumberSetting/index"),
        meta: {
          title: "上传规则设置(todo)",
          permissions: ["super_user", "admin", "super_admin"],
        },
      },
      {
        path: "serialNumSetting",
        name: "serialNumSetting",
        icon: "wallet",
        component: () => import("@/views/serialNumberSetting/index"),
        meta: { title: "编号规则设置" },
      },
    ],
  },
  {
    path: "/manager",
    component: Layout,
    redirect: "noRedirect",
    name: "manager",
    meta: {
      title: "管理",
      icon: "users-cog",
      permissions: ["admin", "super_admin"],
    },
    children: [
      {
        path: "user",
        name: "user",
        component: () => import("@/views/user/index"),
        permissions: ["admin", "super_admin"],
        meta: { title: "用户管理", permissions: ["admin", "super_admin"] },
      },
      {
        path: "analysisModule",
        name: "analysisModule",
        component: () => import("@/views/analysisModule/index"),
        meta: { title: "模块管理", permissions: ["admin", "super_admin"] },
      },
      {
        path: "interface",
        name: "interface",
        component: () => import("@/views/taskInterface/index"),
        meta: {
          title: "接口管理",
          permissions: ["admin", "super_admin"],
          badge: "Pro",
        },
      },
      {
        path: "notification_rule",
        name: "notification_rule",
        component: () => import("@/views/notificationRule/index"),
        meta: {
          title: "消息规则管理",
          permissions: ["admin", "super_admin"],
        },
      },
      {
        path: "announcement",
        name: "announcement",
        component: () => import("@/views/announcement/index"),
        meta: {
          title: "公告管理",
          permissions: ["admin", "super_admin"],
        },
      },
    ],
  },
  {
    path: "*",
    redirect: "/404",
    hidden: true,
  },
];

const router = new VueRouter({
  mode: routerMode,
  scrollBehavior: () => ({
    y: 0,
  }),
  routes: constantRoutes,
});
//注释的地方是允许路由重复点击，如果你觉得框架路由跳转规范太过严格可选择放开
/*const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch((err) => err);
};*/

export function resetRouter() {
  router.matcher = new VueRouter({
    mode: routerMode,
    scrollBehavior: () => ({
      y: 0,
    }),
    routes: constantRoutes,
  }).matcher;
}

export default router;
