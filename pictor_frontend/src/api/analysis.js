/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 分析任务接口
 **/
import request from "@/utils/request";

export function getAnalysisList(params) {
  return request({
    url: "/api/analysis/",
    method: "get",
    params,
  });
}

export function retrieveAnalysis(instance_id) {
  return request({
    url: `/api/analysis/${instance_id}/`,
    method: "get",
  });
}

export function createAnalysis(data) {
  return request({
    url: "/api/analysis/",
    method: "post",
    data,
  });
}

export function deleteAnalysis(instance_id, data) {
  return request({
    url: `/api/analysis/${instance_id}/`,
    method: "delete",
    data,
  });
}

export function updateAnalysis(instance_id, data, method = "put") {
  return request({
    url: `/api/analysis/${instance_id}/`,
    method: method,
    data,
  });
}

export function bulkDeleteAnalysis(data) {
  return request({
    url: `/api/analysis/bulk_delete/`,
    method: "post",
    data,
  });
}

export function getAnalysisStatusList(params) {
  return request({
    url: "/api/analysis/analysis_status/",
    method: "get",
    params,
  });
}

export function getAnalysisStatistics(params) {
  return request({
    url: "/api/analysis/statistics/",
    method: "get",
    params,
  });
}

export function startAnalysis(instance_id, data) {
  return request({
    url: `/api/analysis/${instance_id}/start/`,
    method: "post",
    data,
  });
}

export function stopAnalysis(instance_id, data) {
  return request({
    url: `/api/analysis/${instance_id}/stop/`,
    method: "post",
    data,
  });
}

export function continueRunAnalysis(instance_id, data) {
  return request({
    url: `/api/analysis/${instance_id}/continue_run/`,
    method: "post",
    data,
  });
}

export function resetAnalysis(instance_id, data) {
  return request({
    url: `/api/analysis/${instance_id}/reset/`,
    method: "post",
    data,
  });
}

export function getAnalysisResults(instance_id, params) {
  return request({
    url: `/api/analysis/${instance_id}/results/`,
    method: "get",
    params,
  });
}

export function getAnalysisLogs(instance_id, params) {
  return request({
    url: `/api/analysis/${instance_id}/logs/`,
    method: "get",
    params,
  });
}
