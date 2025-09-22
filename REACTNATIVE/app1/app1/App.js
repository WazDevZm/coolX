import { View, Text, TouchableOpacity } from "react-native";

export default function App() {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#2196f3",
      }}
    >
      <Text
        style={{
          color: "#fff",
          fontSize: 28,
          fontWeight: "bold",
          marginBottom: 20,
          letterSpacing: 1,
        }}
      >
        Welcome to your App, Wazingwa!
      </Text>
      <TouchableOpacity
        style={{
          backgroundColor: "#fff",
          paddingVertical: 12,
          paddingHorizontal: 32,
          borderRadius: 25,
          shadowColor: "#000",
          shadowOffset: { width: 0, height: 2 },
          shadowOpacity: 0.2,
          shadowRadius: 2,
          elevation: 3,
        }}
        onPress={() => alert("Hello, Wazingwa!")}
      >
        <Text style={{ color: "#2196f3", fontWeight: "bold", fontSize: 18 }}>
          Press Me
        </Text>
      </TouchableOpacity>
    </View>
  );
}
