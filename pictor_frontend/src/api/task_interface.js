/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 任务接口设置接口
 **/
import request from "@/utils/request";

export function getAnalysisTaskInterfaceList(params) {
  return request({
    url: "/api/analysis_task_interface/",
    method: "get",
    params,
  });
}

export function retrieveAnalysisTaskInterface(instance_id) {
  return request({
    url: `/api/analysis_task_interface/${instance_id}/`,
    method: "get",
  });
}

export function createAnalysisTaskInterface(data) {
  return request({
    url: "/api/analysis_task_interface/",
    method: "post",
    data,
  });
}

export function deleteAnalysisTaskInterface(instance_id, data) {
  return request({
    url: `/api/analysis_task_interface/${instance_id}/`,
    method: "delete",
    data,
  });
}

export function updateAnalysisTaskInterface(instance_id, data, method = "put") {
  return request({
    url: `/api/analysis_task_interface/${instance_id}/`,
    method: method,
    data,
  });
}

export function bulkDeleteAnalysisTaskInterface(data) {
  return request({
    url: `/api/analysis_task_interface/bulk_delete/`,
    method: "post",
    data,
  });
}

export function activationAnalysisTaskInterface(instance_id, data) {
  return request({
    url: `/api/analysis_task_interface/${instance_id}/activation/`,
    method: "post",
    data,
  });
}

/////////////////////////////////////////////////

export function getSequencingTaskInterfaceList(params) {
  return request({
    url: "/api/seq_task_interface/",
    method: "get",
    params,
  });
}

export function retrieveSequencingTaskInterface(instance_id) {
  return request({
    url: `/api/seq_task_interface/${instance_id}/`,
    method: "get",
  });
}

export function createSequencingTaskInterface(data) {
  return request({
    url: "/api/seq_task_interface/",
    method: "post",
    data,
  });
}

export function deleteSequencingTaskInterface(instance_id, data) {
  return request({
    url: `/api/seq_task_interface/${instance_id}/`,
    method: "delete",
    data,
  });
}

export function updateSequencingTaskInterface(
  instance_id,
  data,
  method = "put"
) {
  return request({
    url: `/api/seq_task_interface/${instance_id}/`,
    method: method,
    data,
  });
}

export function bulkDeleteSequencingTaskInterface(data) {
  return request({
    url: `/api/seq_task_interface/bulk_delete/`,
    method: "post",
    data,
  });
}

export function activationSequencingTaskInterface(instance_id, data) {
  return request({
    url: `/api/seq_task_interface/${instance_id}/activation/`,
    method: "post",
    data,
  });
}
