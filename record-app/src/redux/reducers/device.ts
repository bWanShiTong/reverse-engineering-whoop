import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  device: undefined as string,
  availableDevices: [] as string[],
};

const deviceSlice = createSlice({
  name: "device",
  initialState,
  reducers: {
    addDevice(state, action: { payload: string }) {
      let device = action.payload;
      if (state.availableDevices.find((d) => d === device) === undefined) {
        state.availableDevices.push(device);
      }
    },
    setDevice(state, action: { payload: string }) {
      state.device = action.payload;
      state.availableDevices = [];
    },
  },
});

export const { addDevice, setDevice } = deviceSlice.actions;
export default deviceSlice.reducer;
