/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 项目管理接口
 **/
import request from "@/utils/request";

export function getProjectList(params) {
  return request({
    url: "/api/projects/",
    method: "get",
    params,
  });
}

export function retrieveProject(instance_id) {
  return request({
    url: `/api/projects/${instance_id}/`,
    method: "get",
  });
}

export function createProject(data) {
  return request({
    url: "/api/projects/",
    method: "post",
    data,
  });
}

export function deleteProject(instance_id, data) {
  return request({
    url: `/api/projects/${instance_id}/`,
    method: "delete",
    data,
  });
}

export function updateProject(instance_id, data, method = "put") {
  return request({
    url: `/api/projects/${instance_id}/`,
    method: method,
    data,
  });
}

export function bulkDeleteProject(data) {
  return request({
    url: `/api/projects/bulk_delete/`,
    method: "post",
    data,
  });
}

export function getProjectStatistics(instance_id, params) {
  return request({
    url: `/api/projects/${instance_id}/statistics/`,
    method: "get",
    params,
  });
}
