/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 分析参数接口
 **/
import request from "@/utils/request";

export function getAnalysisParameterList(params) {
  return request({
    url: "/api/analysis_parameters/",
    method: "get",
    params,
  });
}

export function retrieveAnalysisParameter(instance_id) {
  return request({
    url: `/api/analysis_parameters/${instance_id}/`,
    method: "get",
  });
}

export function createAnalysisParameter(data) {
  return request({
    url: "/api/analysis_parameters/",
    method: "post",
    data,
  });
}

export function deleteAnalysisParameter(instance_id, data) {
  return request({
    url: `/api/analysis_parameters/${instance_id}/`,
    method: "delete",
    data,
  });
}

export function updateAnalysisParameter(instance_id, data, method = "put") {
  return request({
    url: `/api/analysis_parameters/${instance_id}/`,
    method: method,
    data,
  });
}

export function bulkDeleteAnalysisParameter(data) {
  return request({
    url: `/api/analysis_parameters/bulk_delete/`,
    method: "post",
    data,
  });
}
