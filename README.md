# Action-Recognition

![CI](https://img.shields.io/github/actions/workflow/status/Eric-YHS/Action-Recognition/ci.yml?branch=main&logo=githubactions&logoColor=white&label=CI)

健身动作识别的资料与原型仓库，收录三条相互独立的内容：基于摄像头姿态估计的动作检测原型
（`camera_pose_prototype/`，本仓库的主要工作）、基于手机六轴传感器的参考实现
（`IndoorHIIT-activity-recognition-master/`，第三方项目），以及两篇中文学位论文 PDF。

| 目录 | 类型 | 说明 |
| --- | --- | --- |
| `camera_pose_prototype/` | 本项目代码 | MediaPipe Pose + 模板匹配的视频动作检测原型 |
| `action/` | 数据 | 9 段标准动作视频（`*.mp4`），用作模板素材与自测输入 |
| `IndoorHIIT-activity-recognition-master/` | 第三方参考 | 微信小程序 + 手机六轴数据 + 随机森林的动作识别与计数项目 |
| `*.pdf` | 第三方文献 | 万鸣华《基于3D姿态估计的动作捕捉和模型驱动方法》、郭天晓《基于人体骨架特征编码的健身动作识别方法》 |

## camera_pose_prototype：摄像头姿态动作检测

流程：视频/摄像头帧 → MediaPipe Pose Landmarker（`data/models/pose_landmarker_lite.task`）
→ 取 17 个关键点（鼻、肩、肘、腕、髋、膝、踝、脚跟、脚尖，见
`pose_motion/constants.py`）→ 世界坐标归一化与旋转对齐 → 关节角度等特征向量
（`pose_motion/features.py`）→ 指数平滑与跳变抑制（`pose_motion/smoothing.py`）→
与预先构建的动作模板逐帧对齐推进并计分（`pose_motion/matcher.py`、
`pose_motion/template_builder.py`）。模板以 JSON 存放在 `data/templates/action_NN.json`。

### 环境

```bash
conda env create -f camera_pose_prototype/environment.yml   # 创建 pose-prototype 环境（Python 3.11）
conda activate pose-prototype
```

依赖为 `mediapipe`、`opencv-python`、`imageio`、`imageio-ffmpeg`（`fastapi`、`uvicorn`
是为后续把原型封装成服务预留的，当前代码尚未使用）。

### 用法

```bash
cd camera_pose_prototype

# 1) 用 ../action 下的标准视频构建模板，输出 data/templates/action_01.json ...
python build_templates.py

# 2) 对视频或摄像头实时检测（--action 从 1 开始，对应模板编号）
python run_detector.py --action 1 --video ../action/xxx.mp4 --display --save-output
python run_detector.py --action 3 --webcam 0 --display --mirror

# 3) 自测：把标准视频当成输入再跑一遍检测，验证模板与匹配逻辑
python self_test.py --repeat 2
```

`run_detector.py` 的常用参数：`--video` / `--webcam` 二选一，`--repeat` 控制视频重复播放次数，
`--mirror` 处理前置摄像头的镜像画面，`--template-dir` 指定模板目录，`--save-output` 输出标注视频。

## IndoorHIIT（第三方参考项目）

山东大学（威海）孙易泽的开源项目：受试者左手持手机，微信小程序实时采集六轴数据，用随机森林模型
与波峰检测法识别并计数「徒手侧平举、前后交叉小跳、开合跳、半蹲」四个动作。原始说明、数据、
 notebook 与代码都在该子目录内，未做修改；详见
[IndoorHIIT-activity-recognition-master/README.md](IndoorHIIT-activity-recognition-master/README.md)。

## 许可

本仓库自研代码（`camera_pose_prototype/`）采用 [MIT 许可](LICENSE)；`action/` 视频、
`IndoorHIIT-activity-recognition-master/` 与两篇论文 PDF 属于第三方材料，版权仍归原作者，
不包含在该 MIT 许可范围内，详见 [LICENSE](LICENSE) 中的第三方声明。
