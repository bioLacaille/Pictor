const state = {
  uploadState: false,
  dataType: false,
  currentPath: false,
  currentTab: false,
};
const getters = {
  uploadState: (state) => state.uploadState,
  dataType: (state) => state.dataType,
  currentPath: (state) => state.currentPath,
  currentTab: (state) => state.currentTab,
};
const mutations = {
  ToUploadState(state, uploadState) {
    state.uploadState = uploadState;
  },
  ToDataType(state, dataType) {
    state.dataType = dataType;
  },
  ToCurrentPath(state, currentPath) {
    state.currentPath = currentPath;
  },
  ToCurrentTab(state, currentTab) {
    state.currentTab = currentTab;
  },
};
const actions = {
  setUploadState({ commit }, data) {
    commit("ToUploadState", data);
  },
  setDataType({ commit }, data) {
    commit("ToDataType", data);
  },
  setCurrentPath({ commit }, data) {
    commit("ToCurrentPath", data);
  },
  setCurrentTab({ commit }, data) {
    commit("ToCurrentTab", data);
  },
  resetUploadState({ commit }) {
    commit("ToUploadState", false);
  },
  resetDataType({ commit }) {
    commit("ToDataType", false);
  },
  resetCurrentPath({ commit }) {
    commit("ToCurrentPath", false);
  },
  resetCurrentTab({ commit }) {
    commit("ToCurrentTab", false);
  },
};
export default { state, getters, mutations, actions };
