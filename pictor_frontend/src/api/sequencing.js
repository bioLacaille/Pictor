/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 拆分任务接口
 * todo: 移除
 **/
import request from "@/utils/request";

export function getSequencingList(params) {
  return request({
    url: "/api/sequencing/",
    method: "get",
    params,
  });
}

export function retrieveSequencing(instance_id) {
  return request({
    url: `/api/sequencing/${instance_id}/`,
    method: "get",
  });
}

export function createSequencing(data) {
  return request({
    url: "/api/sequencing/",
    method: "post",
    data,
  });
}

export function deleteSequencing(instance_id, data) {
  return request({
    url: `/api/sequencing/${instance_id}/`,
    method: "delete",
    data,
  });
}

export function updateSequencing(instance_id, data, method = "put") {
  return request({
    url: `/api/sequencing/${instance_id}/`,
    method: method,
    data,
  });
}

export function bulkDeleteSequencing(data) {
  return request({
    url: `/api/sequencing/bulk_delete/`,
    method: "post",
    data,
  });
}
