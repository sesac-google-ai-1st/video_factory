from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy

# pip install git+https://github.com/huggingface/transformers.git


processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

inputs = processor(
    text=[
        "A song that uses xylophone, triangle, and guitar with a fairy-tale-like clear feel.",
        "The video topic is Pompeii",
    ],
    padding=True,
    return_tensors="pt",
)

audio_values = model.generate(**inputs, max_new_tokens=1500)


sampling_rate = model.config.audio_encoder.sampling_rate
scipy.io.wavfile.write(
    "musicgen_small.wav", rate=sampling_rate, data=audio_values[0, 0].numpy()
)
