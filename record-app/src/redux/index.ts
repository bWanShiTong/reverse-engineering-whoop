import { configureStore } from "@reduxjs/toolkit";
import rootReducer from "./reducers";
import { useSelector } from "react-redux";
import { persistReducer, persistStore } from "redux-persist";
import AsyncStorage from "@react-native-async-storage/async-storage";


const persistedReducer = persistReducer(
  {
    key: "root",
    storage: AsyncStorage,
  },
  rootReducer
);

const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
      immutableCheck: false
    }),
});

export const persistor = persistStore(store);
export default store;

export function selectState(selector: (state: any) => any): any {
  return useSelector(selector);
}
