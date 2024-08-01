# Simple Multi

一个适用于 **Windows** 操作系统，**任何启动器**（只要有实例窗口）的 Minecraft 速通多开工具，具有简易的“墙”。

推荐用于无正版 PCL 等启动器的**较少实例**多开，否则建议购买正版并使用 [Julti](https://github.com/DuncanRuns/Julti)。

只需将若干个实例窗口按照你喜欢的方式在屏幕上排布即可作为“墙”。

（部分代码参考了 [Easy Multi](https://github.com/DuncanRuns/Easy-Multi) 的实现）

## 使用方法

推荐将 失焦自动暂停（pauseOnLostFocus）开启，原因见注意事项 2。

- 根据需要创建若干个 Minecraft 实例（对于 PCL，可以复制出若干个“版本”，**也可以直接使用同一版本多次启动**，但是这样会使得你的存档名出现形如 `Random Speedrun #xxxx (1)` 的格式），将其按照你喜欢的方式在屏幕上排布，并运行 Simple Multi。
  ![](https://github.com/user-attachments/assets/fdbb36e9-66bf-43fa-9ab6-3d274b4af296)
- 点击 `Detect Instances`，下方的 `Current Instances:` 显示的应为你的实例数量。
- 点击 `Start Resetting` 后，保持窗口焦点在 Simple Multi 上，按 T 键即可将所有实例重开（Reset）；若将焦点选中其中一个实例，Simple Multi 会将其自动最大化以供游玩；
- 按下 Atum 模组的重开（Reset）键 F6 或 U 键可以将当前实例重开（Reset），并恢复到原先的窗口状态。
- 重新点击 `Stop Resetting` 即可停止。
- 点击右侧按钮可以更改热键，按 ESC 可以取消。
- obs 录制：可以考虑直接录制显示器（裁剪掉任务栏），墙录制可以直接添加所有窗口的录制。

## 注意事项

- 由于未获取实例路径（且 PCL 一个版本多次启动也没法获取），按 T 键会将**所有实例**重开，而不是 Julti 的设计中的只重开有预览的世界。
- 同上的原因，若未将失焦自动暂停（pauseOnLostFocus）开启，进入其中一个实例后其他实例加载完毕**不会暂停**。
