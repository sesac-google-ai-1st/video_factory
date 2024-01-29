from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy
import torch

# pip install git+https://github.com/huggingface/transformers.git

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"ussing device : {device}")


class musicGen:
    def __init__(self):
        self.processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
        self.model = MusicgenForConditionalGeneration.from_pretrained(
            "facebook/musicgen-small"
        )
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(device)

    def make_bgm(self, user_input):
        user_input = str(user_input)
        inputs = self.processor(
            text=[
                "A song that uses xylophone, triangle, and guitar with a fairy-tale-like clear feel.",
                f"The video topic is {user_input}",
            ],
            padding=True,
            return_tensors="pt",
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}
        audio_values = self.model.generate(**inputs, max_new_tokens=1500)
        audio_values = audio_values.to("cpu")

        sampling_rate = self.model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write(
            f"apps/aieditor/static/audio/musicgen_{user_input}.wav",
            rate=sampling_rate,
            data=audio_values[0, 0].numpy(),
        )
