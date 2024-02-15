from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy
import torch
import os

# pip install git+https://github.com/huggingface/transformers.git


# cuda gpu사용 가능한지 여부 확인
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"BGM using device : {device}")


class musicGen:
    def __init__(self):
        self.processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
        self.model = MusicgenForConditionalGeneration.from_pretrained(
            "facebook/musicgen-small"
        )
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(device)

    def make_bgm(self, user_input_en):
        user_input_en = str(user_input_en)
        inputs = self.processor(
            text=[
                "A song that uses xylophone, triangle, and guitar with a fairy-tale-like clear feel.",
                "Determine the major and minor at first and carefully make it so that the melody can be organically connected.",
                f"The video topic is {user_input_en}",
            ],
            padding=True,
            return_tensors="pt",
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}
        audio_values = self.model.generate(**inputs, max_new_tokens=1500)
        audio_values = audio_values.to("cpu")

        sampling_rate = self.model.config.audio_encoder.sampling_rate

        output_folder = "apps/aieditor/static/audio"
        output_path = os.path.join(output_folder, f"musicgen_{user_input_en}.wav")

        # output_folder가 없으면 만듦
        os.makedirs(output_folder, exist_ok=True)

        scipy.io.wavfile.write(
            output_path,
            rate=sampling_rate,
            data=audio_values[0, 0].numpy(),
        )
