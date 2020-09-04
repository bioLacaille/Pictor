import axios from "axios";
import {
  baseURL,
  contentType,
  messageDuration,
  requestTimeout,
  successCode,
  badRequestCode,
  unAuthCode,
  forbiddenCode,
  notFoundCode,
  errorServerCode,
  debounce,
} from "@/config/settings";
import { Loading, Message } from "element-ui";
import store from "@/store";
import qs from "qs";
import router from "@/router";
import _ from "lodash";

const service = axios.create({
  baseURL,
  timeout: requestTimeout,
  headers: {
    "Content-Type": contentType,
  },
});
let loadingInstance;
service.interceptors.request.use(
  (config) => {
    // 增加 token headers
    if (store.getters["user/accessToken"]) {
      config.headers[
        "Authorization"
      ] = `PICTOR ${store.getters["user/accessToken"]}`;
    }
    console.log("config headers", config.headers["Content-Type"]);
    // 若存在工作区缓存数据, 在参数中加入
    if (store.getters["workzone/workZone"]) {
      // GET
      if (config.method === "get") {
        console.log("config params", config.params);
        if (config.params) {
          config.params["work_zone"] = store.getters["workzone/workZone"].id;
        } else {
          config["params"] = {
            work_zone: store.getters["workzone/workZone"].id,
          };
        }
      } else {
        // POST
        console.log("config data", config.data);
        if (config.data) {
          if (
            config.headers["Content-Type"] ===
            "multipart/form-data;charset=UTF-8"
          ) {
            config.data.append(
              "work_zone",
              store.getters["workzone/workZone"].id
            );
          } else {
            config.data["work_zone"] = store.getters["workzone/workZone"].id;
          }
        } else {
          if (
            config.headers["Content-Type"] ===
            "multipart/form-data;charset=UTF-8"
          ) {
            config.data.append(
              "work_zone",
              store.getters["workzone/workZone"].id
            );
          } else {
            config["data"] = {
              work_zone: store.getters["workzone/workZone"].id,
            };
          }
        }
      }
    }
    // // application/json
    // if (config.headers["Content-Type"] === "application/json;charset=UTF-8") {
    //   if (config.data) {
    //     config.data = _.pickBy(config.data, _.identity);
    //   }
    // }
    // // application/x-www-form-urlencoded
    // if (
    //   config.headers["Content-Type"] ===
    //   "application/x-www-form-urlencoded;charset=UTF-8"
    // ) {
    //   if (config.data && !config.data.param) {
    //     config.data = qs.stringify(config.data);
    //   }
    // }
    // 收否需要显示加载效果
    const needLoading = () => {
      let status = false;
      debounce.forEach((item) => {
        if (_.includes(config.url, item)) {
          status = true;
        }
      });
      return status;
    };
    if (needLoading()) {
      loadingInstance = Loading.service();
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

const errorMsg = (message) => {
  return Message({
    message: message,
    type: "error",
    duration: messageDuration,
  });
};

service.interceptors.response.use(
  (response) => {
    if (loadingInstance) {
      loadingInstance.close();
    }
    const status = response.status;
    const data = response.data;
    if (status !== successCode) {
      return Promise.reject(
        "请求异常拦截:" + JSON.stringify({ data: data }) || "Error"
      );
    } else {
      console.log("response success:", data);
      return data;
    }
  },
  (error) => {
    if (loadingInstance) {
      loadingInstance.close();
    }
    /*网络连接过程异常处理*/
    let { message } = error;
    if (message === "Network Error") {
      errorMsg("Network Error 网络连接异常");
    }
    if (message.includes("timeout")) {
      errorMsg("timeout 接口请求超时");
    }
    console.log("response error:", error);
    if (error.response) {
      const response = error.response;
      const status = response.status;
      const data = response.data;
      const { success, messages, results } = data;
      switch (status) {
        case errorServerCode:
          errorMsg(messages || `后端接口发生 ${status} 异常`);
          break;
        case badRequestCode:
          errorMsg(messages || `当前请求有误!`);
          break;
        case forbiddenCode:
          errorMsg(messages || `当前操作被禁止!`);
          break;
        case unAuthCode:
          errorMsg(messages || `当前登录会话已过期或未登录!请重新登录`);
          store.dispatch("user/resetAccessToken");
          break;
        case notFoundCode:
          router.push({
            path: "/404",
          });
          break;
        default:
          errorMsg(messages || `发生 ${status} 异常`);
          break;
      }
    }
    return Promise.reject(error);
  }
);
export default service;
