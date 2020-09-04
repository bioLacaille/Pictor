import { getWorkZone, removeWorkZone, setWorkZone } from "@/utils/workZone";

const state = {
  workZone: getWorkZone(),
};
const getters = {
  workZone: (state) => state.workZone,
};
const mutations = {
  saveWorkZone(state, workZone) {
    state.workZone = workZone;
    setWorkZone(workZone);
  },
};
const actions = {
  setWorkZone({ commit }, data) {
    commit("saveWorkZone", data);
  },
  resetWorkZone({ commit }) {
    commit("saveWorkZone", "");
    removeWorkZone();
  },
};
export default { state, getters, mutations, actions };
