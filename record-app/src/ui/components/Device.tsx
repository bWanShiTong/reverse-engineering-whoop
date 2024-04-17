import { Text } from "react-native";
import { connectToDevice, scanForDevices } from "../../bluetooth/scan";
import { useEffect, useState } from "react";
import store, { selectState } from "../../redux";
import { manager } from "../../bluetooth";
import { requestBluetoothPermission } from "../../bluetooth/permissions";
import { removeWhoopPackages } from "../../redux/reducers/whoop";
import { Button } from "react-native";
import BackgroundFetch from "react-native-background-fetch";

const Buffer = require("buffer/").Buffer;

async function uploadPackages() {
  let shouldBreak = false;

  while (store.getState().whoop.packages.length > 0 && !shouldBreak) {
    let upload_packages = store.getState().whoop.packages.slice(0, 100);
    await fetch("http://192.168.1.102:5000/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(upload_packages),
    })
      .then((response) => {
        if (response.ok) {
          store.dispatch(removeWhoopPackages(upload_packages));
        }
      })
      .catch(() => (shouldBreak = true));
  }
}

function sendCommand(deviceId: string) {
  manager
    .writeCharacteristicWithoutResponseForDevice(
      deviceId,
      "61080001-8d6d-82b8-614a-1c8cb0f8dcc6",
      "61080002-8d6d-82b8-614a-1c8cb0f8dcc6",
      Buffer.from("aa0c00fc24e417000100000087649e49", "hex").toString("base64")
    )
    .then((char) => {
      delete char["_manager"];
      console.log(JSON.stringify(char, undefined, 4));
    });
}

async function backgroundService(taskId: string) {
  console.log(taskId)
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

async function backgroundServiceTimeout(taskId: string) {
  console.error(taskId);
  BackgroundFetch.finish(taskId);
}

export default function Device() {
  let selectedDevice = selectState((state) => state?.device?.device);
  let [packageCount, setPackageCount] = useState(0);

  function packageCountFunc() {
    setPackageCount(store.getState().whoop.packages.length);
  }

  useEffect(() => {
    BackgroundFetch.configure(
      { minimumFetchInterval: 15 },
      backgroundService,
      backgroundServiceTimeout
    ).then((status) =>
      console.log("[BackgroundFetch] configure status: ", status)
    );
  }, []);

  requestBluetoothPermission();

  useEffect(() => {
    const subscription = manager.onStateChange((state) => {
      if (state === "PoweredOn") {
        scanForDevices();
        subscription.remove();
      }
    }, true);
    return () => subscription.remove();
  }, [manager]);

  useEffect(() => {
    if (selectedDevice) {
      manager.connectedDevices([]).then((devices) => {
        for (let device of devices) {
          if (device.id === selectedDevice) {
            return;
          }
        }

        connectToDevice(selectedDevice);
      });
    }
  }, [selectedDevice]);

  return (
    <>
      <Text>Device: {selectedDevice}</Text>
      <Text>Packages: {packageCount}</Text>
      <Button onPress={packageCountFunc} title="Package count" />
      <Button onPress={uploadPackages} title="Upload" />
      <Button onPress={() => sendCommand(selectedDevice)} title="Send data" />
    </>
  );
}
