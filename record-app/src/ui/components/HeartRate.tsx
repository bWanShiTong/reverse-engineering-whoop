import { Text } from "react-native";
import { selectState } from "../../redux";

export default function HeartRate() {
  let lastReading = selectState((state) => state.heart?.lastReading);

  return (
    <>
      {lastReading?.heartRate && (
        <Text>Heart rate: {lastReading?.heartRate} BPM</Text>
      )}
    </>
  );
}
