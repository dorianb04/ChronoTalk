import os
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
import logging
#from denoiser import denoiser
from tts.text_spliter import prompt_splitter
from pydub import AudioSegment
import sys

import os
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def model_loader():
    """
    Loads the model from the checkpoint and returns the model object
    """
    config = XttsConfig()
    config.load_json("../tts/xtts_2/config.json")
    model = Xtts.init_from_config(config)

    gpu = "cuda" if torch.cuda.is_available() else "cpu"

    if gpu=="cuda":
        model.load_checkpoint(config, checkpoint_dir="../tts/xtts_2/", eval=True)
        model.cuda()
    else:
        model.load_checkpoint(config, checkpoint_dir="../tts/xtts_2/", eval=True)
    logging.info("model_loader: model loaded - using gpu: {gpu}")
    return model


def speaker(model,character_id:str=None):
    """
    input: model object, character_id
    output: gpt_cond_latent, speaker_embedding
    Returns the speaker embedding and the gpt conditioning latent
    """
    src_audios = {"0":"test_audio","1":"01_narrator","2":"02_napoleon","3":"03_bluetooth"} #TODO should be extended to all characters. Might be better to move out of def
    if character_id is None:
        gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["../tts/src_audio/test_audio.wav"])
        logger.info("speaker: character_id is None - using test_audio")
    else:
        gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=[f"../tts/src_audio/{src_audios[character_id]}.wav"])
        logger.info(f"speaker: character_id is {character_id} - using {src_audios[character_id]}")
    return gpt_cond_latent, speaker_embedding


def tts_generator(model, prompt_id:str, text_prompt:str, gpt_cond_latent, speaker_embedding, lang="en"):
    """
    input: model object, prompt_id, text_prompt, gpt_cond_latent, speaker_embedding, lang
    output: audio file
    Generates the audio file from the text prompt
    """
    out = model.inference(
        text_prompt,
        lang,
        gpt_cond_latent,
        speaker_embedding,
        temperature=0.7, # Add custom parameters here
    )
    torchaudio.save(f"../tts/output_audio/{prompt_id}.wav", torch.tensor(out["wav"]).unsqueeze(0), 24000)
    logger.info(f"tts_generator: audio file saved as {prompt_id}.wav")


def tts_api(model, character_id=None,prompt_id=None,text_prompt=None, denoise=False):
    if not character_id:
        logger.error("main: no character_id provided")
    if not prompt_id:
        logger.error("main: no prompt_id provided")
    gpt_cond_latent, speaker_embedding = speaker(model, character_id=character_id)
    tts_generator(model, prompt_id=prompt_id, text_prompt=text_prompt, gpt_cond_latent=gpt_cond_latent, speaker_embedding=speaker_embedding, lang="en")
    #if denoise:
        #denoiser(noisy_audio_path=f"tts/output_audio/{prompt_id}.wav", output_path=f"tts/denoised_audio/{prompt_id}.wav")
    logger.info("main: main completed. character_id: {character_id}, prompt_id: {prompt_id}, denoise: {denoise}")

def main(model, character_id=None, prompt_id=None, text_prompt=None, denoise=False):
    if denoise:
        output_file_path = "denoised_audio"
    else:
        output_file_path = "output_audio"

    if len(text_prompt) > 150:
        prompt_list = prompt_splitter(text_prompt, 150)
        print(prompt_list)
        for i, prompt in enumerate(prompt_list):
            print(i)
            print(prompt)
            tts_api(model, character_id=character_id, prompt_id=prompt_id, text_prompt=prompt, denoise=denoise)
            os.rename(f"../tts/{output_file_path}/{prompt_id}.wav", f"../tts/{output_file_path}/{prompt_id}_{i}.wav")
        
        for i in range(len(prompt_list) - 1):
            # Load the first audio file
            sound1_waveform, sound1_sample_rate = torchaudio.load(f"../tts/{output_file_path}/{prompt_id}_{i}.wav")
            # Load the second audio file
            sound2_waveform, sound2_sample_rate = torchaudio.load(f"../tts/{output_file_path}/{prompt_id}_{i+1}.wav")

            # Check if sample rates are the same
            if sound1_sample_rate != sound2_sample_rate:
                raise ValueError("Sample rates of the audio files do not match.")

            # Concatenate the audio files
            combined_waveform = torch.cat([sound1_waveform, sound2_waveform], dim=1)

            # Save the combined audio file
            torchaudio.save(f"../tts/{output_file_path}/{prompt_id}_{i+1}.wav", combined_waveform, sound1_sample_rate)

        # Rename the last concatenated file to a common name
        os.rename(f"../tts/{output_file_path}/{prompt_id}_{len(prompt_list)-1}.wav", f"../tts/{output_file_path}/{prompt_id}.wav")

        # Remove the individual files, except the combined one
        for i in range(len(prompt_list) - 1):
            os.remove(f"../tts/{output_file_path}/{prompt_id}_{i}.wav")

    else:
        tts_api(model, character_id=character_id, prompt_id=prompt_id, text_prompt=text_prompt, denoise=denoise)

unique_id = "02"
test_prompt = """I was born in Corsica, raised in France, and rose through the ranks of the military. My ambition and strategic mind led me to become a key figure during the French Revolution. Now, I face a crucial decision:
1. Continue my military campaigns to expand French territory.
2. Focus on domestic reforms to strengthen the nation.
3. Negotiate a peace treaty with Britain to avoid further conflict.
4. Collaborate with other European powers to create a new political order. Choose the path that will shape the future of France and Europe."""

if __name__ == "__main__":
    model = model_loader()
    main(model, character_id="2",text_prompt=test_prompt, prompt_id=unique_id)