/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 操作权限接口
 **/
import request from "@/utils/request";

export function getActionPermission(params) {
  return request({
    url: "/api/permissions/",
    method: "get",
    params,
  });
}
