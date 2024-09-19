import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# 设置河流模拟的参数
river_length = 1000  # 河流的总长度（步数）
river_width = 100    # 河流的宽度（单位）
num_points = 200     # 模拟的河流轨迹点数
time_steps = 300     # 动画时间步数

# 生成初始河流轨迹
def generate_river_path(length, num_points, seed=0):
    np.random.seed(seed)
    x = np.linspace(0, length, num_points)
    y = np.cumsum(np.random.randn(num_points))
    return x, y

# 基于正弦和随机噪声生成河流波动
def generate_wave_motion(num_points, time_step):
    wave = np.sin(np.linspace(0, 2 * np.pi, num_points) + time_step / 10) * 10
    noise = np.random.randn(num_points) * 2
    return wave + noise

# 初始化河流路径
x, y = generate_river_path(river_length, num_points)

# 设置绘图
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(0, river_length)
ax.set_ylim(-river_width, river_width)
river_line, = ax.plot([], [], color='deepskyblue', linewidth=3)

# 动态更新函数
def update(frame):
    global y
    y += generate_wave_motion(num_points, frame)
    river_line.set_data(x, y)
    ax.set_title(f"Vltava River Simulation - Time Step: {frame}", fontsize=16, fontweight='bold')
    return river_line,

# 动画
animation = FuncAnimation(fig, update, frames=time_steps, interval=100, blit=True)
plt.show()
