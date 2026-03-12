# 体育部项目

这个仓库目前是一个混合工作区，包含动作识别原型、参考旧项目、样例视频和调研资料。为了方便上传到 GitHub，根目录已经补充了统一的忽略规则和基础说明。

## 目录说明

- `camera_pose_prototype/`：基于 `MediaPipe Pose` 的本地姿态识别原型，用于验证“动作是否标准”和“动作计数”。
- `action/`：原型使用的样例动作视频。
- `IndoorHIIT-activity-recognition-master/`：参考的 `IndoorHIIT` 历史项目，包含 Python 训练代码、微信小程序和原始数据。
- `task.md`：当前任务背景记录。
- 两篇 PDF：动作识别与姿态估计的参考资料。

## 已完成的整理

- 新增根目录 `.gitignore`，统一忽略缓存、IDE 文件、日志和本地生成输出。
- 新增根目录 `.gitattributes`，减少跨平台换行符问题，并标记常见二进制文件。
- 约定不提交以下生成内容：
  - `camera_pose_prototype/outputs/`
  - `_video_contact_sheets/`
  - `_video_contact_sheets_overview.jpg`

## 上传前注意

- `IndoorHIIT-activity-recognition-master/` 看起来来自第三方开源仓库；如果要公开发布，请先确认原仓库许可证和你的使用方式是否匹配。
- 两篇 PDF 如果不是你自己拥有分发权，公开仓库时建议改成外链或在 README 中写参考来源，不要直接二次分发。
- `IndoorHIIT-activity-recognition-master/微信小程序/project.config.json` 中包含历史 `appid`。它通常不是密钥，但如果要继续开发，建议替换成你自己的配置。
- 当前仓库包含数据集和模型文件，整体体积接近 100MB。后续如果继续增大，建议把大文件迁到 Git LFS 或单独的发布资源。

## 建议的 Git 流程

```bash
git init
git branch -M main
git add .
git status
git commit -m "Initial import"
```
