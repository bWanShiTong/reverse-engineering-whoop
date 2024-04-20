import { AppRegistry } from "react-native";
import App from "./App";

import BackgroundFetch from "react-native-background-fetch";

AppRegistry.registerComponent("main", () => App);

async function backgroundService(taskId) {
  console.log(taskId);
  let selectedDevice = store.getState().device.device;
  let devices = await manager.connectedDevices([]);
  for (let device of devices) {
    if (device.id === selectedDevice) {
      BackgroundFetch.finish(taskId);
      return;
    }
  }

  connectToDevice(selectedDevice);
  BackgroundFetch.finish(taskId);
}

async function backgroundServiceTimeout(taskId) {
  console.error(taskId);
  BackgroundFetch.finish(taskId);
}

const backgroundFetchHeadlessTask = async (event) => {
  if (event.timeout) {
    backgroundServiceTimeout(event.taskId);
    return;
  }

  await backgroundService(event.taskId);
};

BackgroundFetch.registerHeadlessTask(backgroundFetchHeadlessTask);
