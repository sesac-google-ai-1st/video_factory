from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy
import torch

# pip install git+https://github.com/huggingface/transformers.git

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"ussing device : {device}")


processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
model = model.to(device)
inputs = processor(
    text=[
        "A song that uses xylophone, triangle, and guitar with a fairy-tale-like clear feel.",
        "The video topic is Pompeii",
    ],
    padding=True,
    return_tensors="pt",
)

inputs = {k: v.to(device) for k, v in inputs.items()}
audio_values = model.generate(**inputs, max_new_tokens=1500)
audio_values = audio_values.to("cpu")

sampling_rate = model.config.audio_encoder.sampling_rate
scipy.io.wavfile.write(
    "musicgen_small.wav", rate=sampling_rate, data=audio_values[0, 0].numpy()
)
