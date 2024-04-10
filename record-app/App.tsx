import { Provider } from "react-redux";
import store, { persistor } from "./src/redux";
import { PersistGate } from "redux-persist/integration/react";
import HeartRate from "./src/ui/components/HeartRate";
import Device from "./src/ui/components/Device";

export default function App() {
  return (
    <Provider store={store}>
      <PersistGate persistor={persistor}>
        <Device />
        <HeartRate />
      </PersistGate>
    </Provider>
  );
}
