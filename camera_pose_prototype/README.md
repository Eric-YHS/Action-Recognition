# Camera Pose Prototype

基于 `MediaPipe Pose + 模板匹配` 的本地原型，用于验证：

- 用户手动选择动作
- 根据摄像头或视频判断动作是否标准
- 对完整动作进行计数

当前目录不依赖旧的传感器识别工程，先单独做本地验证。

## 环境

已按以下环境设计：

- `conda` 环境名：`pose-prototype`
- Python：`3.11`

如果需要重建环境：

```powershell
conda env create -f environment.yml
```

## 目录

- `build_templates.py`：把 `../action` 中的标准视频转成动作模板
- `run_detector.py`：对视频文件或摄像头做动作检测
- `self_test.py`：用标准视频做一轮自测
- `pose_motion/`：原型核心逻辑
- `data/templates/`：生成后的模板文件
- `outputs/`：检测输出目录

## 使用

1. 生成模板

```powershell
conda run -n pose-prototype python build_templates.py
```

2. 检测单个视频

```powershell
conda run -n pose-prototype python run_detector.py --action 1 --video ..\action\3c497234964868a970c812f7e949eecd.mp4 --save-output
```

3. 打开摄像头检测

```powershell
conda run -n pose-prototype python run_detector.py --action 1 --webcam 0
```

4. 自测

```powershell
conda run -n pose-prototype python self_test.py --repeat 2
```

5. 镜像输入测试（实验性）

```powershell
conda run -n pose-prototype python self_test.py --repeat 2 --mirror
```

## 说明

- 当前默认动作名称为 `动作1` 到 `动作9`
- 左右镜像按标准处理
- 判定输出为 `标准 / 不标准`
- 当前算法更偏“先验证可行性”的原型，不是最终部署版
