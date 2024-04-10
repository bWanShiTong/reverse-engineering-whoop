import { createSlice } from "@reduxjs/toolkit";
import { WhoopPackage } from "../../types";

const initialState = {
  packages: [] as WhoopPackage[],
};

const whoopSlice = createSlice({
  name: "heart",
  initialState,
  reducers: {
    addWhoopPackage(state, action: { payload: WhoopPackage }) {
      state.packages.push(action.payload);
    },
    removeWhoopPackages(state, action: { payload: WhoopPackage[] }) {
      state.packages = state.packages.slice(action.payload.length);
    },
  },
});

export const { addWhoopPackage, removeWhoopPackages } = whoopSlice.actions;
export default whoopSlice.reducer;
