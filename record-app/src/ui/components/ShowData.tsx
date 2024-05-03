import { View, Text } from "react-native";
import { useSelector } from "react-redux";
import store from "../../redux";
import { useEffect, useState } from "react";

function showPacket(data: string, index: number) {
  return <Text key={index}>{data}</Text>;
}

function generateData() {
  let index = 0;
  return store
    .getState()
    .whoop.latestPackages.map((packet) => showPacket(packet, index++));
}

export function ShowData() {
  let [data, setData] = useState([]);

  useEffect(() => {
    setInterval(() => {
      setData(generateData());
    }, 1000);
  }, []);

  return (
    <View>
      <Text>Data</Text>
      {data}
    </View>
  );
}
