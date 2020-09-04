import { storage, workZoneTableName } from "@/config/settings";
import cookie from "js-cookie";

// 获取 WorkZone信息
export function getWorkZone() {
  if (storage) {
    if ("localStorage" === storage) {
      return JSON.parse(localStorage.getItem(workZoneTableName));
    } else if ("sessionStorage" === storage) {
      return JSON.parse(sessionStorage.getItem(workZoneTableName));
    } else if ("cookie" === storage) {
      return JSON.parse(cookie.get(workZoneTableName));
    } else {
      return JSON.parse(localStorage.getItem(workZoneTableName));
    }
  } else {
    return JSON.parse(localStorage.getItem(workZoneTableName));
  }
}

//设置 WorkZone信息
export function setWorkZone(workZoneObject) {
  if (storage) {
    if ("localStorage" === storage) {
      return localStorage.setItem(
        workZoneTableName,
        JSON.stringify(workZoneObject)
      );
    } else if ("sessionStorage" === storage) {
      return sessionStorage.setItem(
        workZoneTableName,
        JSON.stringify(workZoneObject)
      );
    } else if ("cookie" === storage) {
      return cookie.set(workZoneTableName, JSON.stringify(workZoneObject));
    } else {
      return localStorage.setItem(
        workZoneTableName,
        JSON.stringify(workZoneObject)
      );
    }
  } else {
    return localStorage.setItem(
      workZoneTableName,
      JSON.stringify(workZoneObject)
    );
  }
}

// 移除 WorkZone信息
export function removeWorkZone() {
  if (storage) {
    if ("localStorage" === storage) {
      return localStorage.removeItem(workZoneTableName);
    } else if ("sessionStorage" === storage) {
      return sessionStorage.clear();
    } else if ("cookie" === storage) {
      return cookie.remove(workZoneTableName);
    } else {
      return localStorage.removeItem(workZoneTableName);
    }
  } else {
    return localStorage.removeItem(workZoneTableName);
  }
}
