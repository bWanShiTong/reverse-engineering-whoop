import { createSlice } from "@reduxjs/toolkit";
import { WhoopPackage } from "../../types";

const LATEST_PACKAGES_SIZE = 5;

const initialState = {
  packages: [] as WhoopPackage[],
  latestPackages: [],
};

const whoopSlice = createSlice({
  name: "heart",
  initialState,
  reducers: {
    addWhoopPackage(state, action: { payload: WhoopPackage }) {
      state.packages.push(action.payload);

      if (!state.latestPackages){
        state.latestPackages = []
      }

      if (action.payload.data.substring(0, 4) == "aa5c") {
        if (state.latestPackages.length >= LATEST_PACKAGES_SIZE) {
          state.latestPackages = state.latestPackages.slice(1, LATEST_PACKAGES_SIZE);
        }
        state.latestPackages.push(action.payload.data);
      }
    },
    removeWhoopPackages(state, action: { payload: WhoopPackage[] }) {
      state.packages = state.packages.slice(action.payload.length);
    },
  },
});

export const { addWhoopPackage, removeWhoopPackages } = whoopSlice.actions;
export default whoopSlice.reducer;
