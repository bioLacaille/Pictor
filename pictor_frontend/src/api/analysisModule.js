/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 分析模块接口
 **/
import request from "@/utils/request";

export function getAnalysisModuleList(params) {
  return request({
    url: "/api/analysis-modules/",
    method: "get",
    params,
  });
}

export function retrieveAnalysisModule(instance_id) {
  return request({
    url: `/api/analysis-modules/${instance_id}/`,
    method: "get",
  });
}

export function createAnalysisModule(
  data,
  headers = { "Content-Type": "application/json;charset=UTF-8" }
) {
  return request({
    url: "/api/analysis-modules/",
    method: "post",
    headers: headers,
    data,
  });
}

export function deleteAnalysisModule(instance_id, data) {
  return request({
    url: `/api/analysis-modules/${instance_id}/`,
    method: "delete",
    data,
  });
}

export function updateAnalysisModule(
  instance_id,
  data,
  method = "put",
  headers = { "Content-Type": "application/json;charset=UTF-8" }
) {
  return request({
    url: `/api/analysis-modules/${instance_id}/`,
    method: method,
    headers: headers,
    data,
  });
}

export function bulkDeleteAnalysisModule(data) {
  return request({
    url: `/api/analysis-modules/bulk_delete/`,
    method: "post",
    data,
  });
}

export function getAnalysisModuleTypes(params) {
  return request({
    url: "/api/analysis-modules/module_types/",
    method: "get",
    params,
  });
}

export function getAnalysisModuleStatus(params) {
  return request({
    url: "/api/analysis-modules/module_status/",
    method: "get",
    params,
  });
}

export function getAnalysisModuleVersions(data) {
  return request({
    url: "/api/analysis-modules/versions/",
    method: "post",
    data,
    timeout: 60000,
  });
}

export function installAnalysisModule(instance_id, data) {
  return request({
    url: `/api/analysis-modules/${instance_id}/install/`,
    method: "post",
    data,
  });
}

export function uninstallAnalysisModule(instance_id, data) {
  return request({
    url: `/api/analysis-modules/${instance_id}/uninstall/`,
    method: "post",
    data,
  });
}

export function stopInstallAnalysisModule(instance_id, data) {
  return request({
    url: `/api/analysis-modules/${instance_id}/stop_install/`,
    method: "post",
    data,
  });
}
