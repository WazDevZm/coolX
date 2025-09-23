
export default function App() {
  return (
    <View style={styles.container}>
      {Platform.OS === 'web' ? (
        <Text style={{ fontSize: 18, color: '#0984e3', textAlign: 'center' }}>
          Welcome! This is the web preview. Camera and native features are only available on mobile (Android/iOS). You should see this message on the web.
        </Text>
      ) : (
        <Text>i.tsx to start working on your app!</Text>
      )}
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
