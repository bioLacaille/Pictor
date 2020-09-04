/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 编号规则设置接口
 **/
import request from "@/utils/request";

export function getAnalysisSerialNumberSettingList(params) {
  return request({
    url: "/api/analysis_nums/",
    method: "get",
    params,
  });
}

export function retrieveAnalysisSerialNumberSetting(instance_id) {
  return request({
    url: `/api/analysis_nums/${instance_id}/`,
    method: "get",
  });
}

export function createAnalysisSerialNumberSetting(data) {
  return request({
    url: "/api/analysis_nums/",
    method: "post",
    data,
  });
}

export function deleteAnalysisSerialNumberSetting(instance_id, data) {
  return request({
    url: `/api/analysis_nums/${instance_id}/`,
    method: "delete",
    data,
  });
}

export function updateAnalysisSerialNumberSetting(
  instance_id,
  data,
  method = "put"
) {
  return request({
    url: `/api/analysis_nums/${instance_id}/`,
    method: method,
    data,
  });
}

export function bulkDeleteAnalysisSerialNumberSetting(data) {
  return request({
    url: `/api/analysis_nums/bulk_delete/`,
    method: "post",
    data,
  });
}

export function activationAnalysisSerialNumberSetting(instance_id, data) {
  return request({
    url: `/api/analysis_nums/${instance_id}/activation/`,
    method: "post",
    data,
  });
}

/////////////////////////////////////////////////

export function getProjectSerialNumberSettingList(params) {
  return request({
    url: "/api/project_nums/",
    method: "get",
    params,
  });
}

export function retrieveProjectSerialNumberSetting(instance_id) {
  return request({
    url: `/api/project_nums/${instance_id}/`,
    method: "get",
  });
}

export function createProjectSerialNumberSetting(data) {
  return request({
    url: "/api/project_nums/",
    method: "post",
    data,
  });
}

export function deleteProjectSerialNumberSetting(instance_id, data) {
  return request({
    url: `/api/project_nums/${instance_id}/`,
    method: "delete",
    data,
  });
}

export function updateProjectSerialNumberSetting(
  instance_id,
  data,
  method = "put"
) {
  return request({
    url: `/api/project_nums/${instance_id}/`,
    method: method,
    data,
  });
}

export function bulkDeleteProjectSerialNumberSetting(data) {
  return request({
    url: `/api/project_nums/bulk_delete/`,
    method: "post",
    data,
  });
}

export function activationProjectSerialNumberSetting(instance_id, data) {
  return request({
    url: `/api/project_nums/${instance_id}/activation/`,
    method: "post",
    data,
  });
}

/////////////////////////////////////////////////

export function getSampleSerialNumberSettingList(params) {
  return request({
    url: "/api/sample_nums/",
    method: "get",
    params,
  });
}

export function retrieveSampleSerialNumberSetting(instance_id) {
  return request({
    url: `/api/sample_nums/${instance_id}/`,
    method: "get",
  });
}

export function createSampleSerialNumberSetting(data) {
  return request({
    url: "/api/sample_nums/",
    method: "post",
    data,
  });
}

export function deleteSampleSerialNumberSetting(instance_id, data) {
  return request({
    url: `/api/sample_nums/${instance_id}/`,
    method: "delete",
    data,
  });
}

export function updateSampleSerialNumberSetting(
  instance_id,
  data,
  method = "put"
) {
  return request({
    url: `/api/sample_nums/${instance_id}/`,
    method: method,
    data,
  });
}

export function bulkDeleteSampleSerialNumberSetting(data) {
  return request({
    url: `/api/sample_nums/bulk_delete/`,
    method: "post",
    data,
  });
}

export function activationSampleSerialNumberSetting(instance_id, data) {
  return request({
    url: `/api/sample_nums/${instance_id}/activation/`,
    method: "post",
    data,
  });
}

/////////////////////////////////////////////////

export function getSequencingSerialNumberSettingList(params) {
  return request({
    url: "/api/sequencing_nums/",
    method: "get",
    params,
  });
}

export function retrieveSequencingSerialNumberSetting(instance_id) {
  return request({
    url: `/api/sequencing_nums/${instance_id}/`,
    method: "get",
  });
}

export function createSequencingSerialNumberSetting(data) {
  return request({
    url: "/api/sequencing_nums/",
    method: "post",
    data,
  });
}

export function deleteSequencingSerialNumberSetting(instance_id, data) {
  return request({
    url: `/api/sequencing_nums/${instance_id}/`,
    method: "delete",
    data,
  });
}

export function updateSequencingSerialNumberSetting(
  instance_id,
  data,
  method = "put"
) {
  return request({
    url: `/api/sequencing_nums/${instance_id}/`,
    method: method,
    data,
  });
}

export function bulkDeleteSequencingSerialNumberSetting(data) {
  return request({
    url: `/api/sequencing_nums/bulk_delete/`,
    method: "post",
    data,
  });
}

export function activationSequencingSerialNumberSetting(instance_id, data) {
  return request({
    url: `/api/sequencing_nums/${instance_id}/activation/`,
    method: "post",
    data,
  });
}
