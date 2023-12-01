#TTS api

import os
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
import logging
from denoiser import denoiser
from text_spliter import prompt_splitter
from pydub import AudioSegment

import uuid #TODO: remove this

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def model_loader(gpu=False):
    """
    Loads the model from the checkpoint and returns the model object
    """
    config = XttsConfig()
    config.load_json("TTS_api/xtts_2/config.json")
    model = Xtts.init_from_config(config)
    if gpu:
        model.load_checkpoint(config, checkpoint_dir="TTS_api/xtts_2/", use_deepspeed=True)
        model.cuda()
    else:
        model.load_checkpoint(config, checkpoint_dir="TTS_api/xtts_2/", use_deepspeed=False)
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
        gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["TTS_api/src_audio/test_audio.wav"])
        logger.info("speaker: character_id is None - using test_audio")
    else:
        gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=[f"TTS_api/src_audio/{src_audios[character_id]}.wav"])
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
    torchaudio.save(f"TTS_api/output_audio/{prompt_id}.wav", torch.tensor(out["wav"]).unsqueeze(0), 24000)
    logger.info(f"tts_generator: audio file saved as {prompt_id}.wav")


def tts_api(character_id=None,prompt_id=None,text_prompt=None, denoise=True):
    if not character_id:
        logger.error("main: no character_id provided")
    if not prompt_id:
        logger.error("main: no prompt_id provided")
    model = model_loader(gpu=False)
    gpt_cond_latent, speaker_embedding = speaker(model, character_id=character_id)
    tts_generator(model, prompt_id=prompt_id, text_prompt=text_prompt, gpt_cond_latent=gpt_cond_latent, speaker_embedding=speaker_embedding, lang="en")
    if denoise:
        denoiser(noisy_audio_path=f"TTS_api/output_audio/{prompt_id}.wav", output_path=f"TTS_api/denoised_audio/{prompt_id}.wav")
    logger.info("main: main completed. character_id: {character_id}, prompt_id: {prompt_id}, denoise: {denoise}")

def main(character_id=None,prompt_id=None,text_prompt=None, denoise=True):
    if len(text_prompt) > 250:
        prompt_list = prompt_splitter(text_prompt)
        for i, prompt in enumerate(prompt_list):
            tts_api(character_id=character_id,prompt_id=prompt_id,text_prompt=prompt, denoise=denoise)
            os.rename(f"TTS_api/denoised_audio/{prompt_id}.wav", f"TTS_api/denoised_audio/{prompt_id}_{i}.wav")
        for i in range(len(prompt_list)):
            if i+1 >= len(prompt_list):
                break
            sound1 = AudioSegment.from_wav(f"TTS_api/denoised_audio/{prompt_id}_{i}.wav")
            sound2 = AudioSegment.from_wav(f"TTS_api/denoised_audio/{prompt_id}_{i+1}.wav")
            combined_sounds = sound1 + sound2
            combined_sounds.export(f"TTS_api/denoised_audio/{prompt_id}_{i+1}.wav", format="wav")
        os.rename(f"TTS_api/denoised_audio/{prompt_id}_{len(prompt_list)-1}.wav", f"TTS_api/denoised_audio/{prompt_id}.wav")
        for i in range(len(prompt_list)-1):
            os.remove(f"TTS_api/denoised_audio/{prompt_id}_{i}.wav")

    else:
        tts_api(character_id=character_id,prompt_id=prompt_id,text_prompt=text_prompt, denoise=denoise)

unique_id = "02"
test_prompt = "On this fateful day at Waterloo, the fate of nations hangs in the balance as my forces clash with the Duke of Wellington and the Prussian forces."     


if __name__ == "__main__":
    main(character_id="1",text_prompt=test_prompt, prompt_id=unique_id)