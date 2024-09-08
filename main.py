import os
from pydub import AudioSegment
import random

def process_audio_files(input_folder, output_folder):
    # 获取文件夹中所有的m4a文件
    audio_files = [f for f in os.listdir(input_folder) if f.endswith('.m4a')]

    # 创建保存处理后音频文件的文件夹
    os.makedirs(output_folder, exist_ok=True)

    for audio_file in audio_files:
        # 加载音频文件
        file_path = os.path.join(input_folder, audio_file)
        audio = AudioSegment.from_file(file_path)

        # 提取左声道（索引为0）
        mono_audio = audio.split_to_mono()[0]

        # 重采样至16kHz
        mono_audio = mono_audio.set_frame_rate(16000)

        # 确定每个音频文件对应的输出文件夹
        audio_output_folder = os.path.join(output_folder, os.path.splitext(audio_file)[0])
        os.makedirs(audio_output_folder, exist_ok=True)

        # 分割音频并保存片段
        duration = len(mono_audio)
        start = 0
        segment_number = 1

        while start < duration:
            # 每个片段长度为15到20秒
            segment_length = random.randint(15000, 20000)  # 生成15秒到20秒之间的随机长度
            end = min(start + segment_length, duration)
            segment = mono_audio[start:end]

            # 保存分割后的片段
            segment_file_name = f"{os.path.splitext(audio_file)[0]}_segment_{segment_number}.wav"
            segment.export(os.path.join(audio_output_folder, segment_file_name), format="wav")

            # 更新起始点和片段编号
            start = end
            segment_number += 1

    print("所有文件处理完成！")

# 设置音频文件所在的文件夹路径
input_folder = "data"

# 设置保存处理后音频文件的文件夹路径
output_folder = "output_data"

# 运行音频处理函数
process_audio_files(input_folder, output_folder)


# 降噪部分
from IPython import display as disp
import torch
import torchaudio
from denoiser import pretrained
from denoiser.dsp import convert_audio
import os
from pydub import AudioSegment
import numpy as np

# 加载预训练的降噪模型
model = pretrained.dns64().cuda()

cnt = 0

def denoise_audio(audio_file_path):
    """对单个音频文件进行降噪处理"""
    wav, sr = torchaudio.load(audio_file_path)
    wav = convert_audio(wav.cuda(), sr, model.sample_rate, model.chin)
    with torch.no_grad():
        denoised = model(wav[None])[0]
    return wav, denoised, model.sample_rate

def process_and_denoise_folder(subfolder_path, output_subfolder_path):
    global cnt
    """对单个子文件夹中的所有音频片段进行处理和降噪"""
    audio_files = [f for f in os.listdir(subfolder_path) if f.endswith('.wav')]
    audio_files.sort()  # 按文件名排序以保证合并顺序

    # 创建对应的输出子文件夹
    os.makedirs(output_subfolder_path, exist_ok=True)

    for audio_file in audio_files:
        file_path = os.path.join(subfolder_path, audio_file)
        
        # 对音频文件进行降噪处理
        wav, denoised, sample_rate = denoise_audio(file_path)
        
        # 展示原始音频和降噪后的音频
        cnt += 1
        # if cnt <= 10:
        #     disp.display(disp.Audio(wav.data.cpu().numpy(), rate=sample_rate))
        #     disp.display(disp.Audio(denoised.data.cpu().numpy(), rate=sample_rate))
        
        # 保存降噪后的音频到对应的输出路径
        output_file_path = os.path.join(output_subfolder_path, audio_file)
        torchaudio.save(output_file_path, denoised.cpu(), sample_rate)

# 设置输入文件夹（output_data）和输出文件夹（output_data_denoised）
input_folder = "./output_data"
output_folder = "./output_data_denoised"

# 处理output_data文件夹中的每个子文件夹
subfolders = [f.path for f in os.scandir(input_folder) if f.is_dir()]

for subfolder in subfolders:
    # 获取相对路径，以便在输出文件夹中创建相应的子文件夹
    relative_path = os.path.relpath(subfolder, input_folder)
    output_subfolder_path = os.path.join(output_folder, relative_path)
    
    process_and_denoise_folder(subfolder, output_subfolder_path)
