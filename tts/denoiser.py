from df.enhance import enhance, init_df, load_audio, save_audio
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def denoiser(noisy_audio_path:str="output_audio/name.wav", output_path:str="enhanced.wav"):
    # Load default model
    model, df_state, _ = init_df()
    # Download and open some audio file. You use your audio files here
    audio_path = noisy_audio_path
    audio, _ = load_audio(audio_path, sr=df_state.sr())
    # Denoise the audio
    enhanced = enhance(model, df_state, audio, atten_lim_db=80)
    # Save for listening
    save_audio(output_path, enhanced, df_state.sr())
    logger.info(f"denoiser: audio denoised - saved as {output_path}")