/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 工作区接口
 **/
import request from "@/utils/request";

export function getWorkZoneList(params) {
  return request({
    url: "/api/work_zones/",
    method: "get",
    params,
  });
}

export function retrieveWorkZone(instance_id) {
  return request({
    url: `/api/work_zones/${instance_id}/`,
    method: "get",
  });
}

export function createWorkZone(data) {
  return request({
    url: "/api/work_zones/",
    method: "post",
    data,
  });
}

export function deleteWorkZone(instance_id, data) {
  return request({
    url: `/api/work_zones/${instance_id}/`,
    method: "delete",
    data,
  });
}

export function updateWorkZone(instance_id, data, method = "put") {
  return request({
    url: `/api/work_zones/${instance_id}/`,
    method: method,
    data,
  });
}

export function getWorkZoneMemberList(instance_id, params) {
  return request({
    url: `/api/work_zones/${instance_id}/members/`,
    method: "get",
    params,
  });
}

export function saveWorkZoneMember(instance_id, data) {
  return request({
    url: `/api/work_zones/${instance_id}/members/`,
    method: "post",
    data,
  });
}

export function getWorkZoneMemberTypes(params) {
  return request({
    url: `/api/work_zones/member_types/`,
    method: "get",
    params,
  });
}

export function validWorkZoneMember(params) {
  return request({
    url: `/api/work_zones/valid/`,
    method: "get",
    params,
  });
}
