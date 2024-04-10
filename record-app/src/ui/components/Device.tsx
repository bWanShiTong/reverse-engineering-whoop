import { Text } from "react-native";
import { connectToDevice, scanForDevices } from "../../bluetooth/scan";
import { useEffect } from "react";
import store, { selectState } from "../../redux";
import { manager } from "../../bluetooth";
import { requestBluetoothPermission } from "../../bluetooth/permissions";
import { removeWhoopPackages } from "../../redux/reducers/whoop";

export default function Device() {
  let selectedDevice = selectState((state) => state?.device?.device);

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
    setInterval(async () => {
      let packages = store.getState().whoop.packages;
      try {
        let response = await fetch("http://192.168.1.102:5000/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(packages),
        });

        if (response.ok) {
          store.dispatch(removeWhoopPackages(packages));
        }
      } catch (e) {
        return;
      }
    }, 5000);
  }, []);

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
    </>
  );
}
