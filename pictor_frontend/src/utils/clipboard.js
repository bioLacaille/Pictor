/**
 Author: Alan Fu
 Email: fualan1990@gmail.com
 * */

import Vue from "vue";
import Clipboard from "clipboard";

function clipboardSuccess() {
  Vue.prototype.$baseMessage("复制成功", "success");
}

function clipboardError() {
  Vue.prototype.$baseMessage("复制失败", "error");
}

// 复制数据
export default function handleClipboard(text, event) {
  const clipboard = new Clipboard(event.target, {
    text: () => text,
  });
  clipboard.on("success", () => {
    clipboardSuccess();
    clipboard.destroy();
  });
  clipboard.on("error", () => {
    clipboardError();
    clipboard.destroy();
  });
  clipboard.onClick(event);
}
