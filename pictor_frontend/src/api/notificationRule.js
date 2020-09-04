/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 站内信箱接口
 **/
import request from "@/utils/request";

export function getNotificationRuleList(params) {
  return request({
    url: "/api/notification_rules/",
    method: "get",
    params,
  });
}

export function retrieveNotificationRule(instance_id) {
  return request({
    url: `/api/notification_rules/${instance_id}/`,
    method: "get",
  });
}

export function createNotificationRule(data) {
  return request({
    url: "/api/notification_rules/",
    method: "post",
    data,
  });
}

export function deleteNotificationRule(instance_id, data) {
  return request({
    url: `/api/notification_rules/${instance_id}/`,
    method: "delete",
    data,
  });
}

export function updateNotificationRule(instance_id, data, method = "put") {
  return request({
    url: `/api/notification_rules/${instance_id}/`,
    method: method,
    data,
  });
}

export function bulkDeleteNotificationRule(data) {
  return request({
    url: `/api/notification_rules/bulk_delete/`,
    method: "post",
    data,
  });
}

export function activationNotificationRule(instance_id, data) {
  return request({
    url: `/api/notification_rules/${instance_id}/activation/`,
    method: "post",
    data,
  });
}
