# denoiser

## 目录结构
├── data/ # 待处理的输入数据文件夹 

├── output_data_denoised/ # 处理后的输出数据文件夹 

├── main.py # 主处理脚本 

├── environment.yml # Conda环境配置文件 

├── README.md # 项目说明文档

## 安装与环境配置

1. **创建虚拟环境**
   本项目依赖于多个Python库，这些库的安装可以通过`environment.yml`文件来配置。首先确保你的系统已经安装了`Conda`。运行以下命令来创建并激活环境：

   ```bash
   conda env create -f environment.yml
   conda activate denoiser  # 替换为环境名

## 使用方法


1. **准备输入数据**
 将待处理的输入数据文件放入data/文件夹中。确保数据格式符合main.py的处理要求。


2. **运行主脚本** 
 运行以下命令来处理数据：
    ```bash
    python main.py

  数据处理完成后，处理后的文件将被保存到output_data_denoised/文件夹中。

## 输出结果
处理后的数据文件将存储在output_data_denoised/文件夹中，文件名与原始输入文件名对应。