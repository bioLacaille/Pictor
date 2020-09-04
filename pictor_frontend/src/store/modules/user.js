/**
 * @description 登录、获取用户信息、退出登录、清除accessToken逻辑，不建议修改
 */

import Vue from "vue";
import { getInfo, login, logout } from "@/api/user";
import { baseURL } from "../../../src/config/settings";
import {
  getAccessToken,
  removeAccessToken,
  setAccessToken,
} from "@/utils/accessToken";
import { resetRouter } from "@/router";
import { title, tokenName } from "@/config/settings";

const state = {
  accessToken: getAccessToken(),
  userName: "",
  nickName: "",
  avatar: "",
  permissions: [],
};
const getters = {
  accessToken: (state) => state.accessToken,
  userName: (state) => state.userName,
  nickName: (state) => state.nickName,
  avatar: (state) => state.avatar,
  permissions: (state) => state.permissions,
};
const mutations = {
  setAccessToken(state, accessToken) {
    state.accessToken = accessToken;
    setAccessToken(accessToken);
  },
  setUserName(state, userName) {
    state.userName = userName;
  },
  setNickName(state, nickName) {
    state.nickName = nickName;
  },
  setAvatar(state, avatar) {
    state.avatar = `${baseURL}${avatar}`;
  },
  setPermissions(state, permissions) {
    state.permissions = permissions;
  },
};
const actions = {
  async login({ commit }, userInfo) {
    console.log("login");
    const data = await login(userInfo);
    const results = data.results;
    console.log(`store login results:`, results);
    const accessToken = results[tokenName];
    if (accessToken) {
      commit("setAccessToken", accessToken);
      const hour = new Date().getHours();
      const thisTime =
        hour < 8
          ? "早上好"
          : hour <= 11
          ? "上午好"
          : hour <= 13
          ? "中午好"
          : hour < 18
          ? "下午好"
          : "晚上好";
      Vue.prototype.$baseNotify(`欢迎登录${title}`, `${thisTime}！`);
    } else {
      Vue.prototype.$baseMessage(
        `登录接口异常，未正确返回${tokenName}...`,
        "error"
      );
    }
  },
  async getInfo({ commit, state }) {
    const data = await getInfo();
    const results = data.results;
    console.log("getInfo results", results);
    if (!data) {
      Vue.prototype.$baseMessage("验证失败，请重新登录...", "error");
      return false;
    }
    commit("setUserName", results.username);
    commit("setNickName", results.nickname);
    commit("setAvatar", results.avatar);
    commit("setPermissions", results.permissions);
    return results.permissions;
  },
  async logout({ dispatch }) {
    await logout(state.accessToken);
    await dispatch("tagsBar/delAllRoutes", null, { root: true });
    await dispatch("resetAccessToken");
    await resetRouter();
  },
  resetAccessToken({ commit }) {
    commit("setPermissions", []);
    commit("setAccessToken", "");
    removeAccessToken();
  },
};
export default { state, getters, mutations, actions };
