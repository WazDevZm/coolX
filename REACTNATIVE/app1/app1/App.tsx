import React from "react";
import {
  View,
  Text,
  Image,
  ScrollView,
  StyleSheet,
  Dimensions,
} from "react-native";

type Program = {
  day: string;
  time: string;
  place: string;
  activity: string;
  inCharge: string;
  image: string;
};

const programs: Program[] = [
  {
    day: "Sunday",
    time: "09:00 - 12:00",
    place: "Main Auditorium",
    activity: "Worship Service",
    inCharge: "PCM Praise Band",
    image:
      "https://images.unsplash.com/photo-1503676382389-4809596d5290?auto=format&fit=crop&w=400&q=80",
  },
  {
    day: "Monday",
    time: "18:00 - 19:30",
    place: "Room 12, Block C",
    activity: "Bible Study",
    inCharge: "Elder Chanda",
    image:
      "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80",
  },
  {
    day: "Tuesday",
    time: "17:30 - 19:00",
    place: "Chapel",
    activity: "Prayer Meeting",
    inCharge: "Prayer Team",
    image:
      "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80",
  },
  {
    day: "Wednesday",
    time: "18:00 - 19:30",
    place: "Room 5, Block A",
    activity: "Outreach Planning",
    inCharge: "Evangelism Team",
    image:
      "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=400&q=80",
  },
  {
    day: "Thursday",
    time: "17:00 - 18:30",
    place: "Chapel",
    activity: "Choir Practice",
    inCharge: "Choir Master",
    image:
      "https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80",
  },
  {
    day: "Friday",
    time: "18:00 - 20:00",
    place: "Main Auditorium",
    activity: "Vespers",
    inCharge: "Youth Band",
    image:
      "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=400&q=80",
  },
  {
    day: "Saturday",
    time: "09:00 - 13:00",
    place: "Main Auditorium",
    activity: "Sabbath Worship & Fellowship",
    inCharge: "PCM Ministry Team",
    image:
      "https://images.unsplash.com/photo-1465101178521-c1a9136a3b43?auto=format&fit=crop&w=400&q=80",
  },
];

const { width } = Dimensions.get("window");

const App: React.FC = () => {
  return (
    <View style={styles.root}>
      <Text style={styles.title}>CBU PCM Campus Ministry</Text>
      <Text style={styles.subtitle}>Weekly Program Schedule</Text>
      <ScrollView
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.scroll}
      >
        {programs.map((prog, idx) => (
          <View key={idx} style={styles.card}>
            <Image source={{ uri: prog.image }} style={styles.image} />
            <View style={styles.info}>
              <Text style={styles.day}>{prog.day}</Text>
              <Text style={styles.activity}>{prog.activity}</Text>
              <Text style={styles.detail}>
                <Text style={styles.label}>Time: </Text>
                {prog.time}
              </Text>
              <Text style={styles.detail}>
                <Text style={styles.label}>Place: </Text>
                {prog.place}
              </Text>
              <Text style={styles.detail}>
                <Text style={styles.label}>In Charge: </Text>
                {prog.inCharge}
              </Text>
            </View>
          </View>
        ))}
      </ScrollView>
    </View>
  );
};

export default App;

const styles = StyleSheet.create({
  root: {
    flex: 1,
    backgroundColor: "#f5f6fa",
    paddingTop: 48,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#0984e3",
    textAlign: "center",
    letterSpacing: 1,
  },
  subtitle: {
    fontSize: 16,
    color: "#636e72",
    textAlign: "center",
    marginBottom: 18,
    letterSpacing: 0.5,
  },
  scroll: {
    alignItems: "center",
    paddingHorizontal: 10,
  },
  card: {
    width: width * 0.85,
    backgroundColor: "#fff",
    borderRadius: 22,
    marginHorizontal: 10,
    marginBottom: 30,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.12,
    shadowRadius: 8,
    elevation: 6,
    overflow: "hidden",
  },
  image: {
    width: "100%",
    height: 170,
    borderTopLeftRadius: 22,
    borderTopRightRadius: 22,
  },
  info: {
    padding: 18,
  },
  day: {
    fontSize: 22,
    fontWeight: "bold",
    color: "#2d3436",
    marginBottom: 4,
  },
  activity: {
    fontSize: 18,
    color: "#0984e3",
    fontWeight: "600",
    marginBottom: 8,
  },
  detail: {
    fontSize: 15,
    color: "#636e72",
    marginBottom: 2,
  },
  label: {
    color: "#636e72",
    fontWeight: "bold",
  },
});
