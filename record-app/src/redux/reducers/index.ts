import { combineReducers } from "@reduxjs/toolkit";

import HearRateReducer from "./heart";
import DeviceReducer from "./device";
import WhoopReducer from "./whoop";

const rootReducer = combineReducers({
  heart: HearRateReducer,
  device: DeviceReducer,
  whoop: WhoopReducer
});

export default rootReducer;
