import { createSlice } from "@reduxjs/toolkit";
import { HeartRateReading } from "../../types";

const initialState = {
  lastReading: undefined as HeartRateReading,
};

const heartSlice = createSlice({
  name: "heart",
  initialState,
  reducers: {
    addHeartRateReading(state, action: { payload: HeartRateReading }) {
      if (state.lastReading?.unix === undefined || state.lastReading.unix < action.payload.unix) {
        state.lastReading = action.payload;
      }
    },
  },
});

export const { addHeartRateReading } = heartSlice.actions;
export default heartSlice.reducer;
