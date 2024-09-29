import SwiftUI
import AVKit
import AVFoundation
import Speech

struct AudioCaptureView: View {
    @State private var audioEngine = AVAudioEngine()
    @State private var recognitionTask: SFSpeechRecognitionTask?
    @State private var recognitionStatus = "Press Start to Record"  // Text for displaying status
    @State private var isRecording = false
    @State private var silenceTimer: Timer?  // Timer to track silence
    @State private var lastRecognitionTime = Date()  // To track the last recognized speech time
    @State private var player: AVPlayer?  // AVPlayer to handle video playback
    
    var body: some View {
        VStack {
            // Video display area, shows only when the video is received
            if let player = player {
                VideoPlayer(player: player)
                    .frame(height: 300)
                    .onAppear {
                        player.play()  // Auto-play video when it appears
                    }
            }

            // Start/Stop Recording Button
            Button(action: {
                if isRecording {
                    stopRecording()
                } else {
                    startRecording()
                }
            }) {
                Text(isRecording ? "Stop Recording" : "Start Recording")
                    .padding()
                    .background(isRecording ? Color.red : Color.green)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }
            .padding()

            // Display the recording status (moved below the button)
            Text(recognitionStatus)
                .padding()
                .foregroundColor(.gray)
                .font(.subheadline)
        }
        .onAppear {
            requestSpeechRecognitionAuthorization()
        }
    }

    func requestSpeechRecognitionAuthorization() {
        SFSpeechRecognizer.requestAuthorization { authStatus in
            DispatchQueue.main.async {
                switch authStatus {
                case .authorized:
                    recognitionStatus = "Speech Recognition Authorized"
                case .denied:
                    recognitionStatus = "Speech Recognition Denied"
                case .restricted:
                    recognitionStatus = "Speech Recognition Restricted"
                case .notDetermined:
                    recognitionStatus = "Speech Recognition Not Determined"
                @unknown default:
                    recognitionStatus = "Unknown Authorization Status"
                }
            }
        }
    }

    func startRecording() {
        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setCategory(.playAndRecord, mode: .measurement, options: .duckOthers)
            try audioSession.setActive(true, options: .notifyOthersOnDeactivation)

            isRecording = true
            recognitionStatus = "Recording in Progress..."
            lastRecognitionTime = Date()
            startListening()  // Start recognizing speech
            startSilenceTimer()  // Start the silence detection timer
        } catch {
            recognitionStatus = "Audio session setup failed"
            print("Audio session setup failed: \(error.localizedDescription)")
        }
    }

    func stopRecording() {
        recognitionTask?.cancel()
        recognitionTask = nil
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)

        isRecording = false
        recognitionStatus = "Recording Stopped"

        // Send recognized text to Flask server
        sendRecognizedTextToServer()
        stopSilenceTimer()
        
        // Fetch video from server
        fetchVideoFromServer()
    }

    func startListening() {
        let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))
        let request = SFSpeechAudioBufferRecognitionRequest()

        guard let recognizer = speechRecognizer, recognizer.isAvailable else {
            recognitionStatus = "Speech recognizer is not available"
            return
        }

        let inputNode = audioEngine.inputNode
        request.shouldReportPartialResults = true

        recognitionTask = recognizer.recognitionTask(with: request) { result, error in
            if let result = result {
                DispatchQueue.main.async {
                    // Update only whether it is still recording or not
                    recognitionStatus = "Recording in Progress..."
                    lastRecognitionTime = Date()  // Reset the last recognition time
                }
            }

            if let error = error {
                DispatchQueue.main.async {
                    recognitionStatus = "Recognition error: \(error.localizedDescription)"
                }
                print("Speech recognition error: \(error.localizedDescription)")
            }
        }

        audioEngine.prepare()

        do {
            try audioEngine.start()
        } catch {
            recognitionStatus = "Audio engine failed to start"
            print("Audio engine failed to start: \(error.localizedDescription)")
        }

        inputNode.installTap(onBus: 0, bufferSize: 1024, format: inputNode.outputFormat(forBus: 0)) { (buffer, _) in
            request.append(buffer)
        }
    }

    // Function to send recognized text to Flask server (dummy text, for demo purposes)
    func sendRecognizedTextToServer() {
        guard let url = URL(string: "http://10.110.227.184:5000/receive-text") else {
            print("Invalid URL")
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let parameters: [String: Any] = [
            "recognizedText": "Some recognized text"
        ]

        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: parameters, options: [])
        } catch let error {
            print("Failed to encode parameters: \(error.localizedDescription)")
            return
        }

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error making POST request: \(error.localizedDescription)")
                return
            }

            guard let data = data else {
                print("No data received from server")
                return
            }

            if let responseString = String(data: data, encoding: .utf8) {
                print("Response from server: \(responseString)")
            }
        }

        task.resume()
    }

    // Fetch video from the server after recording
    func fetchVideoFromServer() {
        guard let url = URL(string: "http://10.110.227.184:5000/video") else {
            print("Invalid video URL")
            return
        }

        let task = URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                print("Error fetching video: \(error.localizedDescription)")
                return
            }

            DispatchQueue.main.async {
                // Assign the URL to AVPlayer and auto-play
                self.player = AVPlayer(url: url)
                self.player?.play()  // Ensure the video starts playing automatically
            }
        }

        task.resume()
    }

    // Start silence timer for 2.5 seconds
    func startSilenceTimer() {
        silenceTimer?.invalidate()  // Invalidate any previous timer
        silenceTimer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { _ in
            let silenceDuration = Date().timeIntervalSince(self.lastRecognitionTime)
            if silenceDuration >= 4.02 {
                self.stopRecording()  // Stop recording if silence is detected for 2.5 seconds
            }
        }
    }

    // Stop the silence timer
    func stopSilenceTimer() {
        silenceTimer?.invalidate()
        silenceTimer = nil
    }
}

struct ContentView: View {
    var body: some View {
        AudioCaptureView()
    }
}

@main
struct asl: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
