#!/usr/bin/env python3

# 必要なライブラリをインポート
import cv2
import subprocess
import boto3
import wave

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)


def makeAudioFile(path, data):
    # オーディオデータから音楽ファイル作成
    wave_data = wave.open(path, 'wb')
    wave_data.setnchannels(1)
    wave_data.setsampwidth(2)
    wave_data.setframerate(16000)
    wave_data.writeframes(data)
    wave_data.close()


rekognition = boto3.client(service_name="rekognition")
translate = boto3.client(service_name="translate")
polly = boto3.client(service_name="polly")


print("[s]キーを押すと画像認識・翻訳・音声合成スタート")
while True:
    # 画像を取得
    success, image = cap.read()
    cv2.imshow("Camera", image)
    key = cv2.waitKey(1)
    if key == ord("s"):
        # カメラ画像を保存する
        image_filename = "camera.png"
        cv2.imwrite(image_filename, image)

        # ----------------------------
        # 画像認識でモノの名前を調べる
        # ----------------------------
        with open(image_filename, "rb") as f:
            detect_label_result = rekognition.detect_labels(
                Image={'Bytes': f.read()},
            )["Labels"]

            # モノが1個以上認識できたら処理を実行
            if len(detect_label_result) > 0:
                # 一番最初に認識したモノの名前を取り出す
                label_name = detect_label_result[0]["Name"]

                # ----------------------------
                # モノの名前を翻訳
                # ----------------------------
                transrate_label_name = translate.translate_text(
                    Text=label_name, SourceLanguageCode="en", TargetLanguageCode="ja"
                )["TranslatedText"]

                print("-----------------------------------------------------")
                print("◯ 翻訳前: {}, 翻訳後: {}".format(label_name, transrate_label_name))
                print("-----------------------------------------------------")

                # ----------------------------
                # 翻訳したモノの名前を音声合成
                # ----------------------------
                speech_data = polly.synthesize_speech(
                    Text=transrate_label_name, OutputFormat="pcm", VoiceId="Mizuki"
                )["AudioStream"]

                # 音声合成のデータを音楽ファイル化
                makeAudioFile("speech.wav", speech_data.read())
                # 保存したWAVデータを再生
                subprocess.check_call('aplay -D plughw:Headphones {}'.format("speech.wav"), shell=True)
