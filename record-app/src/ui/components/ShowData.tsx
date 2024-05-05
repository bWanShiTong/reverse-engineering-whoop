import { View, Text } from "react-native";
import store from "../../redux";
import { useEffect, useState } from "react";
import { decode_aa5c } from "../../bluetooth/services/whoop";
import moment from "moment";

function showPacket(data: string, index: number) {
  let packageData = decode_aa5c(data);
  return (
    <View key={index}>
      <Text>Time: {moment(packageData.unix * 1000).format("DD/MM/YYYY HH:mm:ss")}</Text>
      <Text>Heart rate: {packageData.heartRate}</Text>
    </View>
  );
}

function generateData() {
  let index = 0;
  return store
    .getState()
    .whoop.latestPackages.map((packet) => showPacket(packet, index++));
}

export function ShowData() {
  let [data, setData] = useState([]);

  // useEffect(() => {
  //   setInterval(() => {
  //     setData(generateData());
  //   }, 10000);
  // }, []);

  return (
    <View>
      <Text>Data</Text>
      {/* {data} */}
    </View>
  );
}
