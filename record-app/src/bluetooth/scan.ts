import { manager } from ".";
import store from "../redux";
import { addDevice, setDevice } from "../redux/reducers/device";
import setupServices from "./services";

export function scanForDevices() {
  if (store.getState().device.device === undefined) {
    manager.startDeviceScan(null, null, (error, device) => {
      if (error) {
        console.error(error);
        return;
      }
      if (device) {
        store.dispatch(addDevice(device.id));

        /// proper selecting of device should be added for now it is here
        if (device.name) {
          if (device.name.startsWith("WHOOP")) {
            manager.stopDeviceScan();
            connectToDevice(device.id);
          }
        }
      }
    });
  }
}

export function connectToDevice(deviceId: string) {
  manager
    .connectToDevice(deviceId, { autoConnect: true })
    .then((device) => {
      manager
        .discoverAllServicesAndCharacteristicsForDevice(device.id)
        .then(() => {
          store.dispatch(setDevice(device.id));
          setupServices(device.id);
        });
    })
    .catch((error) => {
      console.error(error);
    });
}
