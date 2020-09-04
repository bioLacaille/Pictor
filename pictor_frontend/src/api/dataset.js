/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 数据集接口
 **/
import request from "@/utils/request";

export function getDataSetList(params) {
  return request({
    url: "/api/dataset/",
    method: "get",
    params,
  });
}

export function retrieveDataSet(instance_id) {
  return request({
    url: `/api/dataset/${instance_id}/`,
    method: "get",
  });
}

export function createDataSet(data) {
  return request({
    url: "/api/dataset/",
    method: "post",
    data,
  });
}

export function deleteDataSet(instance_id, data) {
  return request({
    url: `/api/dataset/${instance_id}/`,
    method: "delete",
    data,
  });
}

export function updateDataSet(instance_id, data, method = "put") {
  return request({
    url: `/api/dataset/${instance_id}/`,
    method: method,
    data,
  });
}

export function bulkDeleteDataSet(data) {
  return request({
    url: `/api/dataset/bulk_delete/`,
    method: "post",
    data,
  });
}

//////////////////////////////////////////////

export function getDataSetType(params) {
  return request({
    url: `/api/dataset/data_types/`,
    method: "get",
    params,
  });
}

export function createDirectoryDataSet(data) {
  return request({
    url: `/api/dataset/create_directory/`,
    method: "post",
    data,
  });
}

export function getDataDirectoryPath(params) {
  return request({
    url: `/api/dataset/directory_path/`,
    method: "get",
    params,
  });
}

export function copyMoveDataSet(data) {
  return request({
    url: `/api/dataset/copy_move/`,
    method: "post",
    data,
  });
}
