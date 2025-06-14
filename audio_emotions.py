import json
import time
import requests
import os

hume_api_key = os.environ.get("HUME_API_KEY")

def analyze_emotion_from_audio(file_path, num_emotions = 3):
    url = "https://api.hume.ai/v0/batch/jobs"
    headers = {
        "X-Hume-Api-Key" : hume_api_key
    }

    payload = {
        "models": {
            "prosody" : {}
        }
    }

    with open(file_path, "rb") as f:
        files = {
            "file": ("audio.wav", f, "audio/wav"),
            "json": (None, json.dumps(payload), "application/json")
        }

        response = requests.post(url, headers = headers, files = files)

    if response.status_code != 200:
        return {"error": "Failed to create job", "details": response.text}
    
    job_id = response.json()["job_id"]
    print(f'Job ID:{job_id}')

    status_url = f"https://api.hume.ai/v0/batch/jobs/{job_id}"

    for _ in range(30):
        time.sleep(2)
        res = requests.get(status_url, headers=headers)
        data = res.json()
        print(f"Job status: {data['state']['status']}")
        if(data['state']["status"] == "COMPLETED"):
            break
        elif(data['state']["status"] == "failed"):
            return{"error": "Job failed", "details": data}
        
    prediction_url = f"https://api.hume.ai/v0/batch/jobs/{job_id}/predictions"
    pred_response = requests.get(prediction_url, headers={
        "X-Hume-Api-Key" : hume_api_key,
        "accept": "application/json; charset = utf-8"
    })

    if(pred_response.status_code != 200):
        return {"error": "Failed to get predictions", "details": pred_response.text}
    
    pred_data = pred_response.json()
    print(f"Predictions recieved: {pred_data}")

    try:
        first_file = pred_data[0]
        grouped = first_file["results"]["predictions"][0]["models"]["prosody"]["grouped_predictions"][0]
        predictions = grouped["predictions"]

        top_prediction = max(predictions, key = lambda p: max(e['score'] for e in p["emotions"]))
        sorted_emotions = sorted(
            top_prediction["emotions"],
            key=lambda e: e["score"],
            reverse=True
        )
        top_emotions = sorted_emotions[:num_emotions]

        return{
            "top_emotions": [
                {"name": e["name"], "score": round(e["score"], num_emotions)} for e in top_emotions
            ],
            "timestamp": top_prediction["time"],
            "raw_emotions": top_prediction["emotions"]
        }
    except Exception as e:
        return {"error": "No valid predictions", "details": str(e)}
    
if __name__ == "__main__":
    AUDIO_PATH = "sample_audio/OAF_base_happy.wav"
    print("Analyzing audio for emotional prosody...")
    result = analyze_emotion_from_audio(AUDIO_PATH)
    print(json.dumps(result, indent=2))