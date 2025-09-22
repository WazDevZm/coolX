
import React, { useRef, useState } from "react";
import { View, Text, TouchableOpacity, StyleSheet, ActivityIndicator, Image } from "react-native";
import { Camera, CameraType } from "expo-camera";
import { SafeAreaView } from "react-native-safe-area-context";

export default function App() {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [photo, setPhoto] = useState<string | null>(null);
  const [result, setResult] = useState<string>("");
  const cameraRef = useRef<Camera>(null);

  React.useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === "granted");
    })();
  }, []);

  const handleCapture = async () => {
    if (cameraRef.current) {
      setIsLoading(true);
      const photoData = await cameraRef.current.takePictureAsync({ base64: true });
      setPhoto(photoData.uri);
      setResult("(Object detection results will appear here)");
      setIsLoading(false);
    }
  };

  if (hasPermission === null) {
    return <View style={styles.center}><ActivityIndicator size="large" color="#0984e3" /></View>;
  }
  if (hasPermission === false) {
    return <View style={styles.center}><Text>No access to camera</Text></View>;
  }

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.header}>Simple Object Detection</Text>
      <View style={styles.cameraContainer}>
        {photo ? (
          <Image source={{ uri: photo }} style={styles.preview} />
        ) : (
          <Camera
            ref={cameraRef}
            style={styles.camera}
            type={CameraType.back}
            ratio="16:9"
          />
        )}
      </View>
      <View style={styles.controls}>
        {photo ? (
          <>
            <TouchableOpacity style={styles.button} onPress={() => setPhoto(null)}>
              <Text style={styles.buttonText}>Retake</Text>
            </TouchableOpacity>
            <Text style={styles.result}>{result}</Text>
          </>
        ) : (
          <TouchableOpacity style={styles.button} onPress={handleCapture} disabled={isLoading}>
            {isLoading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Capture</Text>}
          </TouchableOpacity>
        )}
      </View>
      <Text style={styles.instructions}>
        {photo
          ? "(Detection results will show here after YOLO integration)"
          : "Point your camera at an object and tap Capture."}
      </Text>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f5f6fa",
    paddingHorizontal: 0,
  },
  header: {
    fontSize: 26,
    fontWeight: "bold",
    color: "#0984e3",
    textAlign: "center",
    marginVertical: 18,
    letterSpacing: 1,
  },
  cameraContainer: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    marginHorizontal: 0,
    marginBottom: 10,
  },
  camera: {
    width: "92%",
    aspectRatio: 16 / 9,
    borderRadius: 18,
    overflow: "hidden",
  },
  preview: {
    width: "92%",
    aspectRatio: 16 / 9,
    borderRadius: 18,
    resizeMode: "cover",
  },
  controls: {
    alignItems: "center",
    marginBottom: 10,
  },
  button: {
    backgroundColor: "#0984e3",
    paddingVertical: 14,
    paddingHorizontal: 40,
    borderRadius: 10,
    alignItems: "center",
    marginBottom: 10,
    minWidth: 120,
  },
  buttonText: {
    color: "#fff",
    fontWeight: "bold",
    fontSize: 18,
    letterSpacing: 1,
  },
  result: {
    color: "#636e72",
    fontSize: 16,
    marginTop: 8,
    textAlign: "center",
  },
  instructions: {
    color: "#636e72",
    fontSize: 15,
    textAlign: "center",
    marginBottom: 12,
    marginHorizontal: 12,
  },
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#f5f6fa",
  },
});
