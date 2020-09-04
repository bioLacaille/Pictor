/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 统计数据接口
 **/
import request from "@/utils/request";

export function getStatistic(params) {
  return request({
    url: "/api/statistic/",
    method: "get",
    params,
  });
}
