/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 样本管理接口
 **/
import request from "@/utils/request";

export function getSampleList(params) {
  return request({
    url: "/api/samples/",
    method: "get",
    params,
  });
}

export function retrieveSample(instance_id) {
  return request({
    url: `/api/samples/${instance_id}/`,
    method: "get",
  });
}

export function createSample(data) {
  return request({
    url: "/api/samples/",
    method: "post",
    data,
  });
}

export function deleteSample(instance_id, data) {
  return request({
    url: `/api/samples/${instance_id}/`,
    method: "delete",
    data,
  });
}

export function updateSample(instance_id, data, method = "put") {
  return request({
    url: `/api/samples/${instance_id}/`,
    method: method,
    data,
  });
}

export function bulkDeleteSample(data) {
  return request({
    url: `/api/samples/bulk_delete/`,
    method: "post",
    data,
  });
}

export function relatedSampleFiles(instance_id, data) {
  return request({
    url: `/api/samples/${instance_id}/related_dataset/`,
    method: "post",
    data,
  });
}

export function getRelatedSampleFiles(instance_id, params) {
  return request({
    url: `/api/samples/${instance_id}/related_dataset/`,
    method: "get",
    params,
  });
}

export function getAllRelatedSampleFiles(data) {
  return request({
    url: `/api/samples/all_related_files/`,
    method: "post",
    data,
  });
}
