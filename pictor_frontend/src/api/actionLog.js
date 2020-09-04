/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 操作日志接口
 **/
import request from "@/utils/request";

export function getActionLogList(params) {
  return request({
    url: "/api/action_logs/",
    method: "get",
    params,
  });
}

export function retrieveActionLog(instance_id) {
  return request({
    url: `/api/action_logs/${instance_id}/`,
    method: "get",
  });
}
