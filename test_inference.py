import os
from app.inference import predict

real_dir = "dataset/RealArt"
ai_dir = "dataset/AiArtData"

real_file = os.path.join(real_dir, sorted(os.listdir(real_dir))[0])
ai_file = os.path.join(ai_dir, sorted(os.listdir(ai_dir))[0])

print("Testing:", real_file)
with open(real_file, "rb") as f:
    print("Real image prediction:", predict(f.read()))

print("Testing:", ai_file)
with open(ai_file, "rb") as f:
    print("AI image prediction:", predict(f.read()))
