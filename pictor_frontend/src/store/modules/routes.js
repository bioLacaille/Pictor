/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 路由拦截状态管理，目前两种模式：all模式与intelligence模式
 * 当前仅仅使用了intelligence模式, 可自行开发适配all模式
 */

import { asyncRoutes, constantRoutes } from "@/router";
import { filterAsyncRoutes } from "@/utils/handleRoutes";

const state = { routes: [] };
const getters = {
  routes: (state) => state.routes,
};
const mutations = {
  setRoutes(state, routes) {
    state.routes = constantRoutes.concat(routes);
  },
  setAllRoutes(state, routes) {
    state.routes = constantRoutes.concat(routes);
  },
};
const actions = {
  async setRoutes({ commit }, permissions) {
    let accessedRoutes = [];
    if (permissions.includes("admin")) {
      accessedRoutes = asyncRoutes;
    } else {
      accessedRoutes = await filterAsyncRoutes(asyncRoutes, permissions);
    }
    commit("setRoutes", accessedRoutes);
    return accessedRoutes;
  },
  async setAllRoutes({ commit }) {
    // 可自行开发后端接口，由后端控制路由以及view文件引入
    let accessedRoutes = asyncRoutes;
    commit("setAllRoutes", accessedRoutes);
    return accessedRoutes;
  },
};
export default { state, getters, mutations, actions };
