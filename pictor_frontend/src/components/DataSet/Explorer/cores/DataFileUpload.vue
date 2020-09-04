<template>
  <el-dialog
    title="上传文件(todo: 最小化缩放)"
    :visible.sync="dialogFormVisible"
    width="800px"
    @close="close"
  >
    <div class="file-upload-container">
      <button
        type="button"
        class="btn btn-danger float-right btn-is-option"
        @click.prevent="isOption = !isOption"
      >
        <i class="fa fa-cog" aria-hidden="true"></i>
        设置(todo)
      </button>
      <div v-show="$refs.upload && $refs.upload.dropActive" class="drop-active">
        <h3>Drop files to upload</h3>
      </div>
      <div v-show="!isOption" class="upload">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>名称</th>
                <th>大小</th>
                <th>速度</th>
                <th>状态</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="!files.length">
                <td colspan="7">
                  <div class="text-center p-5">
                    <h4>拖拽文件到此处<br />或者</h4>
                    <label :for="name" class="btn btn-lg btn-primary"
                      >选择文件</label
                    >
                  </div>
                </td>
              </tr>
              <tr v-for="file in files" :key="file.id">
                <td>
                  <div class="filename">
                    {{ file.name }}
                  </div>
                  <div
                    v-if="file.active || file.progress !== '0.00'"
                    class="progress"
                  >
                    <div
                      :class="{
                        'progress-bar': true,
                        'progress-bar-striped': true,
                        'bg-danger': file.error,
                        'progress-bar-animated': file.active,
                      }"
                      role="progressbar"
                      :style="{ width: file.progress + '%' }"
                    >
                      {{ file.progress }}%
                    </div>
                  </div>
                </td>
                <td>{{ file.size }}</td>
                <td>{{ file.speed }}</td>
                <td v-if="file.error">{{ file.error }}</td>
                <td v-else-if="file.success">success</td>
                <td v-else-if="file.active">active</td>
                <td v-else></td>
                <td>
                  <div class="btn-group">
                    <button
                      class="btn btn-secondary btn-sm dropdown-toggle"
                      type="button"
                    >
                      操作
                    </button>
                    <div class="dropdown-menu">
                      <a
                        :class="{
                          'dropdown-item': true,
                          disabled: !file.active,
                        }"
                        href="#"
                        @click.prevent="
                          file.active
                            ? $refs.upload.update(file, {
                                error: 'cancel',
                                active: false,
                              })
                            : false
                        "
                        >取消上传</a
                      >
                      <a
                        v-if="file.active"
                        class="dropdown-item"
                        href="#"
                        @click.prevent="
                          $refs.upload.update(file, { active: false })
                        "
                        >停止上传</a
                      >
                      <a
                        v-else-if="
                          file.error &&
                          file.error !== 'compressing' &&
                          $refs.upload.features.html5
                        "
                        class="dropdown-item"
                        href="#"
                        @click.prevent="
                          $refs.upload.update(file, {
                            active: true,
                            error: '',
                            progress: '0.00',
                          })
                        "
                        >重新上传</a
                      >
                      <a
                        v-else
                        :class="{
                          'dropdown-item': true,
                          disabled:
                            file.success || file.error === 'compressing',
                        }"
                        href="#"
                        @click.prevent="
                          file.success || file.error === 'compressing'
                            ? false
                            : $refs.upload.update(file, { active: true })
                        "
                        >开始上传</a
                      >
                      <div class="dropdown-divider"></div>
                      <a
                        class="dropdown-item"
                        href="#"
                        @click.prevent="$refs.upload.remove(file)"
                        >移除上传</a
                      >
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="example-foorer">
          <div class="footer-status float-right">
            Drop: {{ $refs.upload ? $refs.upload.drop : false }}, Active:
            {{ $refs.upload ? $refs.upload.active : false }}, Uploaded:
            {{ $refs.upload ? $refs.upload.uploaded : true }}, Drop active:
            {{ $refs.upload ? $refs.upload.dropActive : false }}
          </div>
          <div class="btn-group">
            <file-upload
              ref="upload"
              v-model="files"
              class="btn btn-primary dropdown-toggle"
              :extensions="optionForm.accept_extensions"
              :accept="optionForm.accept_mime_type"
              :multiple="optionForm.allow_multiple"
              :directory="optionForm.allow_upload_directory"
              :size="optionForm.max_size || 0"
              :thread="
                optionForm.upload_thread < 1
                  ? 1
                  : optionForm.upload_thread > 5
                  ? 5
                  : optionForm.upload_thread
              "
              :drop="optionForm.allow_drag"
              :drop-directory="optionForm.allow_drag_directory"
              :chunk-enabled="chunkEnabled"
              :chunk="{
                action: postAction,
                headers: headers,
                minSize: chunkMinSize * 1048576,
                maxActive: chunkMaxActive,
                maxRetries: chunkMaxRetries,
              }"
              :headers="headers"
              :data="data"
              :add-index="addIndex"
              @input-filter="inputFilter"
              @input-file="inputFile"
            >
              <i class="fa fa-plus"></i>
              选择文件
            </file-upload>
            <div class="dropdown-menu">
              <label class="dropdown-item" :for="name">文件</label>
              <a class="dropdown-item" href="#" @click="onAddFolader">文件夹</a>
            </div>
          </div>
          <button
            v-if="!$refs.upload || !$refs.upload.active"
            type="button"
            class="btn btn-success"
            @click.prevent="$refs.upload.active = true"
          >
            <i class="fa fa-arrow-up" aria-hidden="true"></i>
            开始上传
          </button>
          <button
            v-else
            type="button"
            class="btn btn-danger"
            @click.prevent="$refs.upload.active = false"
          >
            <i class="fa fa-stop" aria-hidden="true"></i>
            停止上传
          </button>
        </div>
      </div>

      <div v-show="isOption" class="option">
        <el-alert title="设置文件上传规范！不建议修改!" type="warning">
        </el-alert>
        <el-divider></el-divider>
        <div class="form-group">
          <label for="accept_mime_type">文件类型:</label>
          <input
            id="accept_mime_type"
            v-model="optionForm.accept_mime_type"
            type="text"
            class="form-control"
          />
          <small class="form-text text-muted"
            >允许上传的文件类型:<a
              href="https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Basics_of_HTTP/MIME_types"
              target="_blank"
              >MIME 类型</a
            ></small
          >
        </div>
        <div class="form-group">
          <label for="accept_extensions">文件后缀:</label>
          <input
            id="accept_extensions"
            v-model="optionForm.accept_extensions"
            type="text"
            class="form-control"
            placeholder="image/png,image/gif,image/jpeg"
          />
          <small class="form-text text-muted">允许上传的文件后缀</small>
        </div>
        <div class="form-group">
          <label for="upload_thread">线程数:</label>
          <input
            id="upload_thread"
            v-model.number="optionForm.upload_thread"
            type="number"
            max="5"
            min="1"
            class="form-control"
          />
          <small class="form-text text-muted"
            >同时并发上传的文件数量线程数</small
          >
        </div>
        <div class="form-group">
          <label for="max_size">最大限制(B):</label>
          <input
            id="max_size"
            v-model.number="optionForm.max_size"
            type="number"
            min="0"
            class="form-control"
          />
        </div>
        <div class="form-group">
          <label for="min_size">最小限制(B):</label>
          <input
            id="min_size"
            v-model.number="optionForm.min_size"
            type="number"
            min="0"
            class="form-control"
          />
        </div>
        <div class="form-group">
          <div class="form-check">
            <label class="form-check-label">
              <input
                id="allow_multiple"
                v-model="optionForm.allow_multiple"
                type="checkbox"
                class="form-check-input"
              />
              允许选择多个文件
            </label>
          </div>
          <small class="form-text text-muted">是否允许选择多个文件</small>
        </div>
        <div class="form-group">
          <div class="form-check">
            <label class="form-check-label">
              <input
                id="allow_drag"
                v-model="optionForm.allow_drag"
                type="checkbox"
                class="form-check-input"
              />
              允许拖拽
            </label>
          </div>
          <small class="form-text text-muted">是否允许拖拽文件</small>
        </div>
        <div class="form-group">
          <div class="form-check">
            <label class="form-check-label">
              <input
                id="allow_drag_directory"
                v-model="optionForm.allow_drag_directory"
                type="checkbox"
                class="form-check-input"
              />
              允许拖拽文件夹
            </label>
          </div>
          <small class="form-text text-muted">是否允许拖拽文件夹</small>
        </div>
        <div class="form-group">
          <div class="form-check">
            <label class="form-check-label">
              <input
                id="allow_upload_directory"
                v-model="optionForm.allow_upload_directory"
                type="checkbox"
                class="form-check-input"
              />
              允许上传文件夹
            </label>
          </div>
          <small class="form-text text-muted">是否允许上传文件夹</small>
        </div>
        <div class="form-group">
          <div class="form-check">
            <label class="form-check-label">
              <input
                id="auto_upload"
                v-model="optionForm.auto_upload"
                type="checkbox"
                class="form-check-input"
              />
              自动开始上传
            </label>
          </div>
          <small class="form-text text-muted">选择文件后自动开始上传</small>
        </div>
        <div class="form-group">
          <button
            type="button"
            class="btn btn-primary btn-lg btn-block"
            @click.prevent="isOption = !isOption"
          >
            确定
          </button>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script>
import FileUpload from "vue-upload-component";
import store from "@/store";
export default {
  name: "DataFileUpload",
  components: {
    FileUpload,
  },
  data() {
    return {
      dialogFormVisible: false,
      isOption: false, // 是否显示设置
      optionForm: {
        accept_mime_type: "", // 允许上传文件类型 image/png,image/gif,image/jpeg,image/webp
        accept_extensions: "", // 允许上传文件后续 jpg,gif,png,
        upload_thread: 3, // 同时并发上传的文件数量 线程数
        min_size: 1024, // 文件最小限制
        max_size: 1024 * 1024 * 1024, // 文件最大限制
        allow_multiple: true, // 是否允许选择多个文件
        allow_drag: true, // 拖拽上传
        allow_drag_directory: true, // 是否开启拖拽目录
        allow_upload_directory: false, // 是否是上传文件夹
        auto_upload: false, // 是否自动上传
      },
      files: [],
      chunkEnabled: true,
      // 1MB by default
      chunkMinSize: 1,
      chunkMaxActive: 3,
      chunkMaxRetries: 5,
      addIndex: false, // add() 方法 index 参数的默认值
      name: "file", // input标签的 name 属性
      postAction: "http://192.168.1.105:8000/api/datasets/file_part_upload/", // POST 请求的上传URL
      putAction: "http://192.168.1.105:8000/api/datasets/file_part_upload/", // PUT 请求的上传URL
      // 自定义上传请求 header 数据
      headers: { Authorization: `sagene ${store.getters["user/accessToken"]}` },
      // POST 请求: 附加请求的 body
      data: {
        _csrf_token: "xxxxxx",
      },
    };
  },
  watch: {},
  methods: {
    close() {
      this.dialogFormVisible = false;
    },
    showUpload() {
      this.dialogFormVisible = true;
    },
    getUploadConfig() {
      console.log("getUploadConfig ");
    },
    inputFilter(newFile, oldFile, prevent) {
      if (newFile && !oldFile) {
        // Before adding a file Filter system files or hide files
        // 添加文件前 过滤系统文件 和隐藏文件
        if (/(\/|^)(Thumbs\.db|desktop\.ini|\..+)$/.test(newFile.name)) {
          return prevent();
        }
        // Filter php html js file
        // 过滤 php html js 文件
        if (/\.(php5?|html?|jsx?)$/i.test(newFile.name)) {
          this.$baseMessage("不允许上传HTML/PHP/JS文件", "warning");
          return prevent();
        }
      }
    },
    // add, update, remove File Event
    inputFile(newFile, oldFile) {
      console.log("inputFile newFile", newFile);
      console.log("inputFile oldFile", oldFile);
      // 添加文件
      if (newFile && !oldFile) {
        console.log("添加文件");
      }
      // 更新文件
      if (newFile && oldFile) {
        console.log("newFile.active", newFile.active);
        console.log("oldFile.active", oldFile.active);
        // 开始上传
        if (newFile.active && !oldFile.active) {
          console.log("Start upload", newFile.active, newFile);
          // 限定最小字节
          if (
            newFile.size >= 0 &&
            this.optionForm.min_size > 0 &&
            newFile.size < this.optionForm.min_size
          ) {
            this.$refs.upload.update(newFile, { error: "size" });
          }
        }
        console.log("newFile.progress", newFile.progress);
        console.log("oldFile.progress", oldFile.progress);
        // 上传进度
        if (newFile.progress !== oldFile.progress) {
          // progress
          console.log("progress");
        }
        console.log("newFile.error", newFile.error);
        console.log("oldFile.error", oldFile.error);
        // 上传错误
        if (newFile.error && !oldFile.error) {
          // error
          console.log("error");
        }
        console.log("newFile.success", newFile.success);
        console.log("oldFile.success", oldFile.success);
        // 上传成功
        if (newFile.success && !oldFile.success) {
          // success
          console.log("success");
        }
      }
      // 删除文件
      if (!newFile && oldFile) {
        console.log("remove");
        if (oldFile.success && oldFile.response.id) {
          console.log("自动删除 服务器上的文件");
        }
      }
      // 自动上传
      if (
        Boolean(newFile) !== Boolean(oldFile) ||
        oldFile.error !== newFile.error
      ) {
        if (this.optionForm.auto_upload && !this.$refs.upload.active) {
          this.$refs.upload.active = true;
        }
      }
    },
    // add folader
    onAddFolader() {
      if (!this.$refs.upload.features.directory) {
        this.$baseAlert("Your browser does not support");
        return;
      }
      let input = this.$refs.upload.$el.querySelector("input");
      input.directory = true;
      input.webkitdirectory = true;
      this.optionForm.allow_upload_directory = true;
      input.onclick = null;
      input.click();
      input.onclick = (e) => {
        this.optionForm.allow_upload_directory = false;
        input.directory = false;
        input.webkitdirectory = false;
      };
    },
    async uploadActon(file, component) {
      console.log("uploadActon", file);
      console.log("uploadActon component", component);
    },
  },
};
</script>
<style lang="scss" scoped>
@import "../css/font-awesome.min.css";
@import "../css/atom-one-light.min.css";
@import "../css/bootstrap.min.css";
@import "../css/cropper.css";
.file-upload-container .btn-group .dropdown-menu {
  display: block;
  visibility: hidden;
  transition: all 0.2s;
}
.file-upload-container .btn-group:hover > .dropdown-menu {
  visibility: visible;
}

.file-upload-container label.dropdown-item {
  margin-bottom: 0;
}

.file-upload-container .btn-group .dropdown-toggle {
  margin-right: 0.6rem;
}

.file-upload-container .filename {
  margin-bottom: 0.3rem;
}

.file-upload-container .btn-is-option {
  margin-bottom: 1rem;
}
.file-upload-container .example-foorer {
  padding: 0.5rem 0;
  border-top: 1px solid #e9ecef;
  border-bottom: 1px solid #e9ecef;
}

.file-upload-container .edit-image img {
  max-width: 100%;
}

.file-upload-container .edit-image-tool {
  margin-top: 0.6rem;
}

.file-upload-container .edit-image-tool .btn-group {
  margin-right: 0.6rem;
}

.file-upload-container .footer-status {
  padding-top: 0.4rem;
}

.file-upload-container .drop-active {
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  position: fixed;
  z-index: 9999;
  opacity: 0.6;
  text-align: center;
  background: #000;
}

.file-upload-container .drop-active h3 {
  margin: -0.5em 0 0;
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  -webkit-transform: translateY(-50%);
  -ms-transform: translateY(-50%);
  transform: translateY(-50%);
  font-size: 40px;
  color: #fff;
  padding: 0;
}
</style>
