//
//  ContentView.swift
//  asl
//
//  Created by Raudy Brito on 9/28/24.
//

import SwiftUI
import AVFoundation
import Speech
import UIKit
import Starscream

class ViewController: UIViewController, WebSocketDelegate {
    var socket: WebSocket!

    override func viewDidLoad(){
        super.viewDidLoad()
        var request = URLRequest(url: URL(string: "ws://localhost:3001/socket.io/?EIO=4&transport=websocket")!)
        request.timeoutInterval = 5
        socket = WebSocket(request: request)
        socket.delegate = self
        socket.connect()
    }

    func didReceive(event: WebSocketEvent, client: WebSocket){
        switch event{
        case .connected(let headers):
            print("WebSocket is connected: \(headers)")
        case .disconnected(let reason, let code):
            print("WebSocket is disconnected: \(reason) with code: \(code)")
        case .text(let text):
            print("Received text: \(text)")
        case .binary(let data):
            print("Received data: \(data.count)")
        case .ping(_):
            break
        case .pong(_):
            break
        case .viabilityChanged(_):
            break
        case .reconnectSuggested(_):
            break
        case .cancelled:
            print("WebSocket connection cancelled")
        case .error(let error):
            print("WebSocket error: \(String(describing: error))")
        }
    }

    func sendMessage(message: String){
        socket.write(string: message)
    }

    func disconnect(){
        socket.disconnect()
    }
}

struct AudioCaptureView: View {
    @State private var audioRecorder: AVAudioRecorder!
    @State private var audioEngine = AVAudioEngine()
    @State private var recognitionTask: SFSpeechRecognitionTask?
    @State private var isRecording = false
    @State private var recognizedText = ""

    var body: some View {
        VStack {
            Text(recognizedText)
                .padding()
                .foregroundColor(.black)
                .font(.headline)
            
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
        }
        .onAppear {
            requestSpeechRecognitionAuthorization()
        }
    }

    func requestSpeechRecognitionAuthorization() {
        SFSpeechRecognizer.requestAuthorization { authStatus in
            switch authStatus {
            case .authorized:
                print("Speech recognition authorized")
            case .denied:
                print("Speech recognition denied")
            case .restricted, .notDetermined:
                print("Speech recognition not available")
            @unknown default:
                fatalError("Unknown authorization status")
            }
        }
    }

    func startRecording() {
        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setCategory(.playAndRecord, mode: .measurement, options: .duckOthers)
            try audioSession.setActive(true, options: .notifyOthersOnDeactivation)

            isRecording = true
            startListening()
        } catch {
            print("Audio session setup failed: \(error.localizedDescription)")
        }
    }

    func stopRecording() {
        recognitionTask?.cancel()
        recognitionTask = nil
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)

        isRecording = false
    }

    func startListening() {
        let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))
        let request = SFSpeechAudioBufferRecognitionRequest()

        guard let recognizer = speechRecognizer, recognizer.isAvailable else {
            print("Speech recognizer is not available")
            return
        }

        let inputNode = audioEngine.inputNode
        request.shouldReportPartialResults = true

        recognitionTask = recognizer.recognitionTask(with: request) { result, error in
            if let result = result {
                recognizedText = result.bestTranscription.formattedString
                tokenizeAndSendData(text: recognizedText)
            }
            
            if let error = error {
                print("Speech recognition error: \(error.localizedDescription)")
            }
        }

        audioEngine.prepare()

        do {
            try audioEngine.start()
        } catch {
            print("Audio engine failed to start: \(error.localizedDescription)")
        }

        inputNode.installTap(onBus: 0, bufferSize: 1024, format: inputNode.outputFormat(forBus: 0)) { (buffer, _) in
            request.append(buffer)
        }
    }

    func tokenizeAndSendData(text: String) {
        let words = text.split(separator: " ").map { String($0) }
        sendToWebhook(words: words)
    }

    func sendToWebhook(words: [String]) {
        guard let url = URL(string: "https://your-webhook-url.com") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let json: [String: Any] = ["words": words]
        request.httpBody = try? JSONSerialization.data(withJSONObject: json)

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error sending data: \(error.localizedDescription)")
                return
            }
            print("Data sent successfully")
        }
        task.resume()
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

struct AudioCaptureView_Previews: PreviewProvider {
    static var previews: some View {
        AudioCaptureView()
    }
}
