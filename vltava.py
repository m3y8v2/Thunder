import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
import noise  # 用于生成Perlin噪声
import random
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D

# 生成地形的函数
def generate_terrain(size, scale=50, octaves=6, persistence=0.5, lacunarity=2.0, seed=0):
    np.random.seed(seed)
    terrain = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            terrain[i][j] = noise.pnoise2(i / scale, 
                                          j / scale, 
                                          octaves=octaves, 
                                          persistence=persistence, 
                                          lacunarity=lacunarity, 
                                          repeatx=size, 
                                          repeaty=size, 
                                          base=seed)
    return terrain

# 定义河流生成规则
def generate_river_path(terrain, start_point, path_length, seed=0):
    np.random.seed(seed)
    size = terrain.shape[0]
    path = [start_point]
    current_point = start_point
    for _ in range(path_length):
        x, y = current_point
        # 获取周围点中最低的点
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        valid_neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < size and 0 <= ny < size]
        next_point = min(valid_neighbors, key=lambda p: terrain[p[0], p[1]])
        path.append(next_point)
        current_point = next_point
        # 防止河流陷入局部最低点
        if len(path) > 10 and len(set(path[-10:])) == 1:
            break
    return path

# 可视化地形和河流
def plot_terrain_with_river(terrain, river_paths):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    x = np.linspace(0, terrain.shape[0], terrain.shape[0])
    y = np.linspace(0, terrain.shape[1], terrain.shape[1])
    x, y = np.meshgrid(x, y)
    ax.plot_surface(x, y, terrain, cmap=cm.terrain, alpha=0.7)

    # 绘制河流路径
    for path in river_paths:
        px = [p[0] for p in path]
        py = [p[1] for p in path]
        pz = [terrain[p[0], p[1]] for p in path]
        ax.plot(px, py, pz, color='blue', linewidth=2)
    
    # 设置视角和标签
    ax.view_init(elev=60, azim=-30)
    ax.set_title("Terrain with River Paths", fontsize=16)
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_zlabel("Height")
    plt.show()

# 动态河流展示
def animate_rivers(terrain, river_paths, time_steps):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, terrain.shape[0])
    ax.set_ylim(0, terrain.shape[1])
    ax.imshow(terrain, cmap='Greens', extent=[0, terrain.shape[0], 0, terrain.shape[1]])
    
    # 初始化河流绘制
    river_lines = []
    for _ in river_paths:
        line, = ax.plot([], [], color='blue', linewidth=2)
        river_lines.append(line)
    
    # 动态更新函数
    def update(frame):
        for line, path in zip(river_lines, river_paths):
            if frame < len(path):
                px = [p[0] for p in path[:frame]]
                py = [p[1] for p in path[:frame]]
                line.set_data(px, py)
        return river_lines
    
    animation = FuncAnimation(fig, update, frames=time_steps, interval=100, blit=True)
    plt.show()

# 地形和河流参数
terrain_size = 100
terrain_scale = 25
path_length = 200
num_rivers = 3

# 生成地形
terrain = generate_terrain(terrain_size, scale=terrain_scale, seed=random.randint(0, 100))

# 生成多条河流
river_paths = []
for _ in range(num_rivers):
    start_x = random.randint(0, terrain_size-1)
    start_y = random.randint(0, terrain_size-1)
    river_path = generate_river_path(terrain, (start_x, start_y), path_length, seed=random.randint(0, 100))
    river_paths.append(river_path)

# 可视化地形和河流
plot_terrain_with_river(terrain, river_paths)

# 动态展示河流演化过程
animate_rivers(terrain, river_paths, time_steps=100)
