<template>
  <div>
    <div class="elp-header-wrap">
      <div class="elp-header-img">
        <span>
          <img :src="current_user.avatar" />
        </span>
        <span>
          <div>{{ this_time }}，{{ current_user.nickname }}，欢迎使用系统</div>
          <div>
            {{ current_user.role_zh }} | {{ current_user.email }} |
            {{ current_user.gender }} |
            {{ current_user.title }}
          </div>
        </span>
      </div>
      <div class="elp-header-extra">
        <div>
          <div>项目数</div>
          <div>{{ project_count }}</div>
        </div>
        <div>
          <div>样本数</div>
          <div>{{ sample_count }}</div>
        </div>
        <div>
          <div>分析任务数</div>
          <div>{{ analysis_count }}</div>
        </div>
      </div>
    </div>
    <el-divider content-position="center">
      <i class="el-icon-mobile-phone"></i><el-tag type="primary">项目</el-tag>
    </el-divider>
    <div class="elp-card-grid">
      <div class="elp-card-grid-body">
        <div
          v-for="project in project_list"
          :key="project.id"
          class="elp-card-grid-item-wrap"
        >
          <div class="elp-card-grid-item">
            <div>
              <img src="@/assets/project.png" />
              <el-button type="text" size="medium" @click="handleMange(project)"
                >{{ project.serial_number }}({{ project.name }})</el-button
              >
            </div>
            <div style="word-break: break-all">{{ project.remark }}</div>
            <div>
              <span>{{ project.creator.nickname }}</span>
              <span>{{ project.created_time }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <el-divider content-position="center">
      <i class="el-icon-mobile-phone"></i
      ><el-tag type="primary">分析任务</el-tag>
    </el-divider>
    <div class="elp-card-grid">
      <div class="elp-card-grid-body">
        <div
          v-for="analysis in analysis_list"
          :key="analysis.id"
          class="elp-card-grid-item-wrap"
        >
          <div class="elp-card-grid-item">
            <div>
              <img src="@/assets/analysis.jpeg" />
              <el-button
                type="text"
                size="medium"
                @click="handleShowAnalysis(analysis)"
                >{{ analysis.serial_number }}</el-button
              >
            </div>
            <div>
              {{ analysis.analysis_module.name }}@{{
                analysis.analysis_module.version
              }}
            </div>
            <div>
              <span
                ><el-tag :type="StatusTagFilter(analysis.status)">
                  <p>{{ statusOptions[analysis.status] }}</p>
                </el-tag></span
              >
              <span>{{ analysis.created_time }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <el-divider content-position="center">
      <i class="el-icon-mobile-phone"></i
      ><el-tag type="primary"
        >工作区动态(todo:目前为整个系统的动态, 后续增加区分)</el-tag
      >
    </el-divider>
    <div class="elp-list-and-card">
      <div class="elp-list-wrap">
        <elp-card title="工作区动态">
          <div
            v-for="action_log in action_log_list"
            :key="action_log.id"
            class="elp-list-item"
          >
            <div class="elp-list-item-avatar">
              <img
                width="40"
                height="40"
                :src="`${base_url}${action_log.user.avatar}`"
              />
            </div>
            <div class="elp-list-item-content">
              <div class="elp-list-item-content-title">
                <span>{{ action_log.user.username }}</span> IP
                <span>{{ action_log.remote_ip }}</span> 操作
                <span>{{ action_log.action_info }}</span>
              </div>
              <div class="elp-list-item-content-date">
                {{ action_log.created_time }}
              </div>
            </div>
          </div>
        </elp-card>
      </div>
      <div class="elp-work-group">
        <elp-card title="工作区成员">
          <div class="elp-work-group-wrap">
            <div
              v-for="work_zone_user in work_zone_user_list"
              :key="work_zone_user.user.id"
              class="elp-work-group-item"
            >
              <img
                width="30"
                height="30"
                :src="`${base_url}${work_zone_user.user.avatar}`"
              />
              <span>{{ work_zone_user.user.nickname }}</span>
              <span
                ><el-tag
                  size="medium"
                  :type="filerLevelColor(work_zone_user.level)"
                >
                  {{ member_types[work_zone_user.level] }}
                </el-tag></span
              >
            </div>
          </div>
        </elp-card>
      </div>
    </div>
    <project-manage ref="manage_project"></project-manage>
    <show-analysis ref="show_analysis"></show-analysis>
  </div>
</template>
<script>
import ElpCard from "./components/ElpCard.vue";
import { getActionLogList } from "@/api/actionLog";
import { getInfo } from "@/api/user";
import { getStatistic } from "@/api/statistic";
import { getProjectList } from "@/api/project";
import { getWorkZoneMemberList, getWorkZoneMemberTypes } from "@/api/workzone";
import { getAnalysisList, getAnalysisStatusList } from "@/api/analysis";
import { baseURL } from "../../../src/config/settings";
import ShowAnalysis from "../analysis/components/ShowAnalysis";
import ProjectManage from "../project/components/ProjectManage";
import store from "@/store";
export default {
  components: {
    ElpCard,
    ShowAnalysis,
    ProjectManage,
  },
  data() {
    return {
      base_url: baseURL,
      current_user: {
        id: "",
        username: "",
        nickname: "",
        avatar: "",
        email: "",
        role_zh: "",
        gender: "",
        phone: "",
        title: "",
        address: "",
        remark: "",
        role_level: "",
      },
      project_count: 0,
      sample_count: 0,
      analysis_count: 0,
      this_time: new Date().getHours(),
      project_list: [],
      analysis_list: [],
      statusOptions: {},
      action_log_list: [],
      work_zone_user_list: [],
      member_types: {},
    };
  },
  mounted() {},
  created() {
    this.fetchAnalysisStatus();
    this.getMemberTypes();
    this.getThisTime();
    this.getUserInfo();
    this.statistic();
    this.fetchProjectList();
    this.fetchAnalysisList();
    this.fetchActionLogList();
    this.fetchWorkZoneUsers();
  },
  methods: {
    handleShowAnalysis(row) {
      this.$refs["show_analysis"].show(row);
    },
    handleMange(row) {
      this.$refs["manage_project"].showMange(row);
    },
    getThisTime() {
      const hour = new Date().getHours();
      this.this_time =
        hour < 8
          ? "早上好"
          : hour <= 11
          ? "上午好"
          : hour <= 13
          ? "中午好"
          : hour < 18
          ? "下午好"
          : "晚上好";
    },
    async getUserInfo() {
      const data = await getInfo();
      const results = data.results;
      this.current_user = Object.assign(
        {},
        {
          id: results.id,
          username: results.username,
          nickname: results.nickname,
          role_zh: results.role_zh,
          avatar: `${baseURL}${results.avatar}`,
          email: results.email,
          gender: results.gender,
          phone: results.phone,
          title: results.title,
          address: results.address,
          remark: results.remark,
          role_level: results.role_level,
        }
      );
    },
    async statistic() {
      const data = await getStatistic();
      const results = data.results;
      this.project_count = results.project_count;
      this.sample_count = results.sample_count;
      this.analysis_count = results.analysis_count;
    },
    async fetchProjectList() {
      this.listLoading = true;
      const data = await getProjectList();
      this.project_list = data.results;
      setTimeout(() => {
        this.listLoading = false;
      }, 500);
    },
    async fetchAnalysisList() {
      this.listLoading = true;
      const data = await getAnalysisList();
      this.analysis_list = data.results;
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
    async fetchAnalysisStatus() {
      this.listLoading = true;
      const data = await getAnalysisStatusList();
      this.statusOptions = data.results;
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
    async fetchActionLogList() {
      this.listLoading = true;
      const data = await getActionLogList();
      this.action_log_list = data.results;
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
    async fetchWorkZoneUsers() {
      this.listLoading = true;
      const work_zone_id = store.getters["workzone/workZone"].id;
      const data = await getWorkZoneMemberList(work_zone_id);
      this.work_zone_user_list = data.results;
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
    async getMemberTypes() {
      this.listLoading = true;
      const data = await getWorkZoneMemberTypes({ zh: true });
      this.member_types = data.results;
      setTimeout(() => {
        this.listLoading = false;
      }, 300);
    },
    /**
     * @return {string}
     */
    StatusTagFilter(val) {
      if (val < 10) {
        return "danger";
      }
      if (val < 20) {
        return "info";
      }
      if (val < 30) {
        return "";
      }
      if (val < 40) {
        return "warning";
      }
      if (val < 50) {
        return "danger";
      }
      if (val < 60) {
        return "success";
      }
      return "danger";
    },
    filerLevelColor(level) {
      if (level === 10) {
        return "success";
      } else if (level === 20) {
        return "info";
      } else if (level === 30) {
        return "warning";
      } else if (level === 40) {
        return "danger";
      } else {
        return "success";
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.elp-header-wrap {
  background: #fff;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  .elp-header-img {
    display: flex;
    img {
      height: 74px;
      width: 74px;
      border-radius: 50%;
    }
    > :nth-child(2) {
      margin-left: 20px;
      :first-child {
        line-height: 38px;
        font-size: 18px;
      }
      :last-child {
        line-height: 40px;
        font-size: 14px;
        color: #666;
      }
    }
  }
  .elp-header-extra {
    display: flex;
    flex-direction: row;
    > div {
      border-right: 1px #eee solid;
      :first-child {
        color: #666;
      }
      div {
        text-align: center;
        padding: 8px 14px;
      }
    }
    :last-child {
      border-right: none;
    }
  }
}

.elp-card-grid {
  margin-top: 20px;
  background: #fff;
  padding: 20px 20px;
  .elp-card-grid-head {
    line-height: 50px;
    border-bottom: 1px #eee solid;
  }
  .elp-card-grid-body {
    color: #999;
    height: 100%;
    display: flex;
    flex-wrap: wrap;
    flex: 1 1 0;
    .elp-card-grid-item-wrap {
      width: 25%;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      padding-top: 10px;
      padding-left: 10px;
      word-break: break-all;
      .elp-card-grid-item {
        border-bottom: 1px #eee solid;
        padding: 20px;
        > div:first-child {
          display: flex;
          align-items: center;
          color: #333;
          width: 100%;
          img {
            width: 24px;
            height: 24px;
            border-radius: 50%;
          }
          span {
            display: inline-block;
            margin-left: 10px;
            line-height: 24px;
          }
          margin-bottom: 20px;
        }
        > div:nth-child(2) {
          font-size: 14px;
        }
        > div:last-child {
          font-size: 12px;
          margin-top: 20px;
          display: flex;
          justify-content: space-between;
        }
      }
    }

    .elp-card-grid-item-wrap:nth-child(n) {
      .elp-card-grid-item {
        border-top: 1px #eee solid;
        border-left: 1px #eee solid;
        border-right: 1px #eee solid;
      }
    }
    .elp-card-grid-item-wrap:nth-child(4) {
      .elp-card-grid-item {
        border-right: 1px #eee solid;
      }
    }
  }
}
.elp-list-and-card {
  display: flex;
  margin-top: 10px;
  .elp-list-wrap {
    width: 100%;
    .elp-list-item {
      display: flex;
      border-bottom: 1px #eee solid;
      padding: 14px;
      color: #666;
      .elp-list-item-avatar {
        width: 40px;
        height: 40px;
        img {
          border-radius: 50%;
        }
      }
      .elp-list-item-content {
        padding-left: 20px;
        line-height: 26px;
        .elp-list-item-content-title {
          span:nth-child(2) {
            color: #3892f7;
          }
          span:nth-child(3) {
            color: #3892f7;
          }
        }
        .elp-list-item-content-date {
          color: #999;
        }
      }
    }
  }
  .elp-work-group {
    margin-left: 10px;
    width: 40%;
    .elp-work-group-wrap {
      display: flex;
      flex-wrap: wrap;
      color: #666;
      span {
        margin-left: 10px;
      }
      .elp-work-group-item {
        display: flex;
        align-items: center;
        padding: 10px 0;
        width: 50%;
        img {
          margin-left: 20px;
          border-radius: 50%;
        }
      }
    }
  }
}
@media only screen and (max-width: 1350px) {
  .elp-card-grid .elp-card-grid-body .elp-card-grid-item-wrap {
    width: 50%;
    &:nth-child(2) {
      .elp-card-grid-item {
        border-right: 1px #eee solid;
      }
    }
  }
}
@media only screen and (max-width: 1100px) {
  .elp-list-and-card {
    display: block;
    .elp-work-group {
      margin-left: 0;
      width: 100%;
    }
  }
}
@media only screen and (max-width: 950px) {
  .elp-header-wrap {
    display: block;
    .elp-header-extra {
      margin-top: 20px;
    }
  }
}
@media only screen and (max-width: 800px) {
  .elp-header-wrap {
    .elp-header-img {
      display: block;
    }
    .elp-header-extra {
      margin-top: 0;
    }
  }
  .elp-card-grid .elp-card-grid-body .elp-card-grid-item-wrap {
    width: 100%;
    &:nth-child(n) {
      .elp-card-grid-item {
        border-right: 1px #eee solid;
      }
    }
  }
}
@media only screen and (max-width: 600px) {
  .elp-card-grid {
    .elp-card-grid-body {
      display: block;
    }
  }
}
</style>
