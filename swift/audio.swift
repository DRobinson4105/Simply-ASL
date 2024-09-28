//
//  audio.swift
//  asl
//
//  Created by Raudy Brito on 9/28/24.
//

import UIKit
import AVFoundation
import Speech


class AudioCaptureViewController: UIViewController, AVAudioRecorderDelegate {
    var audioRecorder: AVAudioRecorder!

    override func viewDidLoad() {
        super.viewDidLoad()
        startRecording()
    }

    func startRecording() {
        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setCategory(.playAndRecord, mode: .default)
            try audioSession.setActive(true)
            let recordingURL = getDocumentsDirectory().appendingPathComponent("recording.m4a")
            let settings = [
                AVFormatIDKey: Int(kAudioFormatAppleLossless),
                AVSampleRateKey: 44100,
                AVNumberOfChannelsKey: 2,
                AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
            ]
            audioRecorder = try AVAudioRecorder(url: recordingURL, settings: settings)
            audioRecorder.delegate = self
            audioRecorder.record()
        } catch {
            print("Failed to set up recording: \(error.localizedDescription)")
        }
    }

    func getDocumentsDirectory() -> URL {
        let paths = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)
        return paths[0]
    }
    
    func startListening() {
            let recognizer = SFSpeechRecognizer()
            let request = SFSpeechAudioBufferRecognitionRequest()
            
            let audioEngine = AVAudioEngine()
            let inputNode = audioEngine.inputNode
            
            inputNode.installTap(onBus: 0, bufferSize: 1024, format: inputNode.outputFormat(forBus: 0)) { (buffer, when) in
                request.append(buffer)
            }
            
            audioEngine.prepare()
            
            do {
                try audioEngine.start()
                recognizer?.recognitionTask(with: request, resultHandler: { (result, error) in
                    if let result = result {
                        let recognizedText = result.bestTranscription.formattedString
                        print("Recognized Text: \(recognizedText)")
                        self.tokenizeAndSendData(text: recognizedText)
                    }
                    if let error = error {
                        print("Recognition error: \(error.localizedDescription)")
                    }
                })
            } catch {
                print("Audio Engine Error: \(error.localizedDescription)")
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
