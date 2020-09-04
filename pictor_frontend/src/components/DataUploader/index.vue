<template>
  <div v-if="uploadState" id="global-uploader">
    <div class="enlarge">
      <div class="file-title">
        <div>上传文件(todo: 并发上传)</div>
        <div class="operate">
          <el-button
            type="text"
            :title="collapse ? '展开' : '折叠'"
            @click="fileListShow"
          >
            <i
              :class="collapse ? 'el-icon-folder-add' : 'el-icon-folder-remove'"
            ></i>
          </el-button>

          <el-button type="text" title="关闭" @click="close">
            <i class="el-icon-close"></i>
          </el-button>
        </div>
      </div>
      <!-- 上传 -->
      <div v-show="showUpload" class="upload-bottom">
        <uploader
          ref="uploader"
          :options="options"
          :auto-start="true"
          :file-status-text="fileStatusText"
          class="uploader-app"
          @file-added="onFileAdded"
          @file-success="onFileSuccess"
          @file-progress="onFileProgress"
          @file-error="onFileError"
          @file-submitted="filesSubmitted"
        >
          <uploader-unsupport></uploader-unsupport>
          <div class="but-upload">
            <uploader-drop style="padding: 10%; margin-left: 3%;">
              <p>Drop files here to upload or</p>
              <uploader-btn
                id="global-uploader-btn"
                ref="uploadBtn"
                :attrs="attrs"
                size="mini"
                type="primary"
                >选择文件</uploader-btn
              >
              <uploader-btn
                id="global-uploader-btn-folder"
                ref="uploadBtnFolder"
                :directory="true"
                :attrs="attrs"
                size="mini"
                type="primary"
                >选择文件夹</uploader-btn
              >
            </uploader-drop>
          </div>
          <uploader-list v-show="panelShow">
            <div
              slot-scope="props"
              class="file-panel"
              :class="{ collapse: collapse }"
            >
              <ul class="file-lists">
                <li
                  v-for="file in props.fileList"
                  :key="file.id"
                  class="upload-list-file"
                >
                  <uploader-file
                    ref="files"
                    :class="'file_' + file.id"
                    :file="file"
                    :list="true"
                  ></uploader-file>
                </li>
                <div v-if="!props.fileList.length" class="no-file">
                  <i class="iconfont icon-empty-file"></i> 暂无待上传文件
                </div>
              </ul>
            </div>
          </uploader-list>
        </uploader>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * Author: Alan Fu
 * Email: fualan1990@gmail.com
 * 文件上传 组件
 **/
import SparkMD5 from "spark-md5";
import store from "@/store";
import { baseURL } from "../../../src/config/settings";

export default {
  mame: "DataUploader",
  //注册局部组件指令
  directives: {
    drag: function (el) {
      let dragBox = el; //获取当前元素
      dragBox.onmousedown = (e) => {
        //算出鼠标相对元素的位置
        let disX = e.clientX - dragBox.offsetLeft;
        let disY = e.clientY - dragBox.offsetTop;
        document.onmousemove = (e) => {
          //用鼠标的位置减去鼠标相对元素的位置，得到元素的位置
          let left = e.clientX - disX;
          let top = e.clientY - disY;
          //移动当前元素
          dragBox.style.right = dragBox.offsetWidth - left + "px";
          dragBox.style.bottom = dragBox.offsetHeight - top + "px";
        };
        document.onmouseup = (e) => {
          //鼠标弹起来的时候不再移动
          document.onmousemove = null;
          //预防鼠标弹起来后还会循环（即预防鼠标放上去的时候还会移动）
          document.onmouseup = null;
        };
      };
    },
  },
  data() {
    return {
      // 上传选项
      options: {
        target: `${baseURL}/api/dataset/file_upload/`,
        chunkSize: "1048576", // 1M
        fileParameterName: "file",
        maxChunkRetries: 3, // 最大自动失败重试上传次数，值可以是任意正整数，如果是 undefined 则代表无限次，默认 0
        simultaneousUploads: 1, //并发上传数 todo: 后端暂时不接收并发上传, 后续更新
        testChunks: true, //是否开启服务器分片校验
        // 服务器分片校验函数，秒传及断点续传基础
        checkChunkUploadedByResponse: function (chunk, response_data) {
          let objMessage = JSON.parse(response_data);
          if (objMessage.results.uploaded) {
            return true;
          }
          let uploaded_chunks = objMessage.results.uploaded_chunks.indexOf(
            chunk.offset + 1
          );
          return uploaded_chunks >= 0;
        },
        // 处理请求结果
        processResponse: function (response, cb, File, chunk) {
          let objMessage = JSON.parse(response);
          if (!objMessage.success) {
            cb(true, File.error);
          } else {
            cb(null, response);
          }
        },
        processParams(params) {
          //每一次分片传给后台的参数，params是该方法返回的形参，包含分片信息
          console.log("processParams", params);
          return {
            //返回一个对象，会添加到每一个分片的请求参数里面
            data_type: store.getters["uploader/dataType"],
            current_path: store.getters["uploader/currentPath"],
            work_zone: store.getters["workzone/workZone"].id,
            chunk_index: params.chunkNumber,
            chunk_size: params.chunkSize,
            current_chunk_size: params.currentChunkSize,
            total_size: params.totalSize,
            file_md5: params.identifier,
            file_name: params.filename,
            relative_path: params.relativePath,
            total_chunks: params.totalChunks,
          };
        },
        headers: {
          Authorization: `PICTOR ${store.getters["user/accessToken"]}`, // todo 第一次打开时获取有误,需要解决
        },
        parseTimeRemaining: function (timeRemaining, parsedTimeRemaining) {
          return parsedTimeRemaining
            .replace(/\syears?/, "年")
            .replace(/\days?/, "天")
            .replace(/\shours?/, "小时")
            .replace(/\sminutes?/, "分钟")
            .replace(/\sseconds?/, "秒");
        },
        successStatuses: [200, 201, 202],
        permanentErrors: [400, 401, 402, 403, 404, 415, 500, 501, 502],
      },
      attrs: { accept: "" }, // 限制可上传的文件格式
      fileStatusText(status, response) {
        const statusTextMap = {
          uploading: "上传中",
          paused: "暂停",
          waiting: "等待中",
        };
        if (status === "success") {
          return "上传成功";
        } else if (status === "error") {
          return "上传失败";
        } else {
          return statusTextMap[status];
        }
      },
      panelShow: false, //选择文件后，展示上传panel
      collapse: false,
      showUpload: true,
      maxSize: 1024 * 1024 * 1024, // 大小限制
    };
  },
  computed: {
    //Uploader实例
    uploader() {
      console.log("this.uploader", this.$refs.uploader.uploader);
      return this.$refs.uploader.uploader;
    },
    // 弹窗状态
    uploadState: {
      get: function () {
        return store.getters["uploader/uploadState"];
      },
    },
  },
  watch: {
    type: {
      handler: function (val) {},
      deep: true,
      immediate: true,
    },
  },
  methods: {
    filesSubmitted(files, fileList, event) {
      console.log("filesSubmitted", files, fileList, event);
    },
    removeFile(file) {
      console.log("removeFile", file);
    },
    onFileAdded(file, event) {
      console.log("onFileAdded", file, event);
      this.panelShow = true;
      file.pause();
      if (file) {
        console.log(file.size);
        let isLt2M = file.size < this.maxSize;
        if (!isLt2M) {
          file.cancel();
          file.ignored = true;
          this.$baseAlert(`上传文件大小不能超过 ${this.maxSize}`);
        } else {
          this.computeMD5(file);
        }
      }
    },
    onFileProgress(rootFile, file, chunk) {
      console.log("onFileProgress", rootFile, file, chunk);
    },
    onFileSuccess(rootFile, file, response, chunk) {
      console.log("onFileSuccess", rootFile, file, response, chunk);
      let res = JSON.parse(response);
      if (res.results.uploaded) {
        this.$emit("getForFileList");
      }
    },
    onFileError(rootFile, file, response, chunk) {
      this.$message({
        message: "上传失败",
        type: "error",
      });
    },

    /**
     * 计算md5，实现断点续传及秒传
     * @param file
     */
    computeMD5(file) {
      let fileReader = new FileReader();
      let time = new Date().getTime();
      let blobSlice =
        File.prototype.slice ||
        File.prototype.mozSlice ||
        File.prototype.webkitSlice;
      let currentChunk = 0;
      const chunkSize = 10 * 1024 * 1000;
      let chunks = Math.ceil(file.size / chunkSize);
      let spark = new SparkMD5.ArrayBuffer();

      // 文件状态设为"计算MD5"
      // this.statusSet(file.id, "md5");
      file.pause();
      loadNext();
      fileReader.onload = (e) => {
        spark.append(e.target.result);
        if (currentChunk < chunks) {
          currentChunk++;
          loadNext();
          // 实时展示MD5的计算进度
          this.$nextTick(() => {});
        } else {
          let md5 = spark.end();
          this.computeMD5Success(md5, file);
        }
      };

      fileReader.onerror = function () {
        this.$baseMessage(`文件${file.name}读取出错，请检查该文件`, "error");
        file.cancel();
      };

      function loadNext() {
        let start = currentChunk * chunkSize;
        let end =
          start + chunkSize >= file.size ? file.size : start + chunkSize;

        fileReader.readAsArrayBuffer(blobSlice.call(file.file, start, end));
      }
    },

    computeMD5Success(md5, file) {
      // 将自定义参数直接加载uploader实例的opts上
      Object.assign(this.uploader.opts, {
        query: {
          ...this.params,
        },
      });
      file.uniqueIdentifier = md5;
      file.resume();
    },
    //收缩
    fileListShow() {
      let _this = this;
      _this.collapse = !_this.collapse;
      _this.showUpload = !this.showUpload;
    },
    //关闭
    close() {
      let upState = this.uploader.isUploading();
      let isComplete = this.uploader.isComplete();
      this.uploader.cancel();
      store.dispatch("uploader/resetUploadState");
    },
  },
};
</script>

<style scoped lang="scss">
#global-uploader {
  position: fixed;
  z-index: 3000;
  right: 15px;
  bottom: 15px;
  background-color: #fff;
  border: 1px solid #e2e2e2;
  border-radius: 7px 7px 0 0;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  cursor: move;
  ::v-deep .uploader-file-name {
    text-align: left;
  }
  ::v-deep .uploader-file-icon {
    display: none;
  }
  .enlarge {
    width: 650px;
    overflow: auto;
  }
  .file-title {
    display: flex;
    height: 40px;
    line-height: 40px;
    padding: 0 15px;
    border-bottom: 1px solid #ddd;
    .operate {
      flex: 1;
      text-align: right;
    }
  }
  .overFlow-hidden {
    min-height: 500px;
    max-height: 650px;
  }
  ::v-deep .el-button--text {
    padding: 0 10px;
  }
  ::v-deep .uploader-file-icon {
    &:before {
      content: "" !important;
    }

    &[icon="image"] {
      background: none;
    }
    // &[icon="video"] {
    //   background: center / contain no-repeat url(../../common/video.png);
    // }
    //   &[icon=document] {
    //       background: url(../images/text-icon.png);
    //   }
  }
  .uploader-app {
    overflow: auto;
    padding-right: 20px;
  }
  .but-upload {
    text-align: center;
    margin-top: 10px;
    margin-bottom: 10px;
  }
  .upload-bottom {
    height: 500px;
    overflow: auto;
  }
  .file-panel {
    .file-title {
      display: flex;
      height: 40px;
      line-height: 40px;
      padding: 0 15px;
      border-bottom: 1px solid #ddd;

      .operate {
        flex: 1;
        text-align: right;
      }
    }

    .file-lists {
      position: relative;
      // height: 540px;
      overflow-x: hidden;
      overflow-y: auto;
      background-color: #fff;
      > li {
        background-color: #fff;
      }
    }

    &.collapse {
      .file-title {
        background-color: #cfd7e5;
      }
    }
  }

  .no-file {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 16px;
  }

  ul,
  li {
    list-style: none;
  }
  .header-list {
    display: flex;
    justify-content: flex-start;
    margin-top: 10px;
    padding: 0 20px;
  }
  .total-num {
    font-size: 14px;
    color: #606266;
    height: 32px;
    line-height: 32px;
    margin-right: 20px;
    width: 200px;
  }
}
/* 隐藏上传按钮 */
#global-uploader-btn {
  // position: absolute;
  // clip: rect(0, 0, 0, 0);
  background: #409eff;
  color: #fff;
  border: none;
  margin-left: 20px;
  font-size: 14px;
}

/* 隐藏上传按钮 */
#global-uploader-btn-folder {
  // position: absolute;
  // clip: rect(0, 0, 0, 0);
  background: #409eff;
  color: #fff;
  border: none;
  margin-left: 20px;
  font-size: 14px;
}
::v-deep .uploader-file-actions > span {
  margin-right: 6px;
}
.submit-bot {
  text-align: center;
  margin: 10px 0;
}
.upload-list-file {
  position: relative;
}
.file-img {
  position: absolute;
  top: 0;
  left: 0;
  width: 40px;
  height: 40px;
}
</style>
