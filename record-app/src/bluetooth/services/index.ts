import { manager } from "..";
import store from "../../redux";
import { addHeartRateReading } from "../../redux/reducers/heart";
import { addWhoopPackage } from "../../redux/reducers/whoop";
import { readHeartRateData } from "./heart";

const Buffer = require("buffer/").Buffer;

export default function setupServices(deviceId: string) {
  manager.monitorCharacteristicForDevice(
    deviceId,
    "0000180d-0000-1000-8000-00805f9b34fb",
    "00002a37-0000-1000-8000-00805f9b34fb",
    (error, payload) => {
      if (error) {
        if (error.errorCode != 201) {
          console.error(error);
        }
        return;
      }

      let unix = Math.round(Date.now() / 1000);
      let buffer = Buffer.from(payload.value, "base64");
      let heartRateReading = readHeartRateData(buffer);

      store.dispatch(
        addHeartRateReading({
          unix,
          heartRate: heartRateReading.heartRate,
        })
      );
    }
  );

  manager.monitorCharacteristicForDevice(
    deviceId,
    "61080001-8d6d-82b8-614a-1c8cb0f8dcc6",
    "61080005-8d6d-82b8-614a-1c8cb0f8dcc6",
    (error, payload) => {
      if (error) {
        if (error.errorCode != 201) {
          console.error(error);
        }
        return;
      }
      let unix = Math.round(Date.now() / 1000);
      let data = Buffer.from(payload.value, "base64").toString("hex");
      store.dispatch(
        addWhoopPackage({
          unix,
          data,
          characteristic: "61080005-8d6d-82b8-614a-1c8cb0f8dcc6",
        })
      );
    }
  );

  manager.monitorCharacteristicForDevice(
    deviceId,
    "61080001-8d6d-82b8-614a-1c8cb0f8dcc6",
    "61080005-8d6d-82b8-614a-1c8cb0f8dcc6",
    (error, payload) => {
      if (error) {
        if (error.errorCode != 201) {
          console.error(error);
        }
        return;
      }

      let unix = Math.round(Date.now() / 1000);
      let data = Buffer.from(payload.value, "base64").toString("hex");
      store.dispatch(
        addWhoopPackage({
          unix,
          data,
          characteristic: "61080005-8d6d-82b8-614a-1c8cb0f8dcc6",
        })
      );
    }
  );
}
