
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from matplotlib.animation import FuncAnimation

# 1. PARAMETERS AND CONFIGURATION
R = 1.0
r = R * np.sqrt(3) / 2
CLUSTER_SIZE = 7

# Frequency groups A to G
FREQ_GROUPS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Different colors for frequency groups
COLOR_MAP = {
    'A': '#FF9999',
    'B': '#99FF99',
    'C': '#9999FF',
    'D': '#FFFF99',
    'E': '#FFCC99',
    'F': '#99FFFF',
    'G': '#E599FF'
}

# Coordinates of the seven cells
CLUSTER_BASE = [
    (0.0, 0.0),
    (2 * r, 0.0),
    (r, 1.5 * R),
    (-r, 1.5 * R),
    (-2 * r, 0.0),
    (-r, -1.5 * R),
    (r, -1.5 * R)
]

# Positions of three clusters
D_X = 7.0
CLUSTER_OFFSETS = [
    (-D_X, 0),
    (0, 0),
    (D_X, 0)
]

# 2. CREATE THE CELLULAR NETWORK
cells = []

for ox, oy in CLUSTER_OFFSETS:
    for idx, (bx, by) in enumerate(CLUSTER_BASE):
        cells.append({
            'x': bx + ox,
            'y': by + oy,
            'freq': FREQ_GROUPS[idx]
        })

# 3. INITIALIZE THE PLOT
fig, ax = plt.subplots(figsize=(15, 8))


# Function to draw a hexagonal cell
def draw_cell(x, y, freq, alpha=0.6,
              border_color='black', lw=1.2):

    hexagon = RegularPolygon(
        (x, y),
        numVertices=6,
        radius=R,
        orientation=np.radians(30),
        edgecolor=border_color,
        facecolor=COLOR_MAP.get(freq, '#CCCCCC'),
        alpha=alpha,
        linewidth=lw
    )

    ax.add_patch(hexagon)

    # Draw base station and frequency label
    ax.plot(x, y, 'k^', markersize=4)

    ax.text(
        x, y + 0.15, freq,
        fontsize=10,
        fontweight='bold',
        ha='center',
        va='center'
    )


# Draw all cells in the network
for cell in cells:
    draw_cell(cell['x'], cell['y'], cell['freq'])


# 4. HIGHLIGHT FREQUENCY REUSE DISTANCE
# Find cells using frequency group A
a_cells = [
    (c['x'], c['y'])
    for c in cells
    if c['freq'] == 'A'
]

# Draw dashed lines between reused A cells
for i in range(len(a_cells) - 1):
    x1, y1 = a_cells[i]
    x2, y2 = a_cells[i + 1]

    ax.plot(
        [x1, x2],
        [y1, y2],
        'k--',
        linewidth=1.5,
        label='Reuse Distance (D)' if i == 0 else ""
    )


# 5. DEMONSTRATE CO-CHANNEL INTERFERENCE
# Create two adjacent cells using frequency A
INCORRECT_OFFSET_X = 13.5

wrong_cluster = [
    ('A', (INCORRECT_OFFSET_X, 0.0)),
    ('A', (INCORRECT_OFFSET_X + 2 * r, 0.0)),
    ('C', (INCORRECT_OFFSET_X + r, 1.5 * R)),
    ('E', (INCORRECT_OFFSET_X - r, 1.5 * R))
]

# Draw the incorrectly assigned cells in red
for freq, (x, y) in wrong_cluster:
    draw_cell(
        x, y, freq,
        alpha=0.85,
        border_color='red',
        lw=1.8
    )

# Highlight interference between adjacent A cells
ax.plot(
    [INCORRECT_OFFSET_X, INCORRECT_OFFSET_X + 2 * r],
    [0, 0],
    'r-',
    linewidth=3.5,
    label='Co-Channel Interference'
)

ax.text(
    INCORRECT_OFFSET_X + r,
    -1.0,
    "SEVERE INTERFERENCE!\n(Adjacent 'A' cells)",
    color='red',
    fontweight='bold',
    fontsize=9,
    ha='center'
)


# 6. MOBILE USER AND HANDOVER ANIMATION
frames_count = 160

# Mobile user moves horizontally
path_x = np.linspace(-10, 10, frames_count)
path_y = np.zeros(frames_count)

# Mobile user dot and movement trail
user_dot, = ax.plot(
    [], [], 'ko',
    markersize=8,
    zorder=5,
    label='Mobile User'
)

user_path_line, = ax.plot(
    [], [],
    'k:',
    linewidth=1,
    alpha=0.5
)

# Display connection information
status_box = ax.text(
    -10.5, 5.0, "",
    fontsize=10,
    bbox=dict(
        boxstyle='round',
        facecolor='white',
        alpha=0.9
    )
)


# Update mobile user position in every frame
def update(frame):
    x = path_x[frame]
    y = path_y[frame]

    # Update user position and trail
    user_dot.set_data([x], [y])

    user_path_line.set_data(
        path_x[:frame + 1],
        path_y[:frame + 1]
    )

    # Calculate distance from user to each base station
    distances = [
        np.sqrt(
            (x - c['x'])**2 +
            (y - c['y'])**2
        )
        for c in cells
    ]

    # Find the nearest base station
    nearest_idx = np.argmin(distances)
    serving_bs = cells[nearest_idx]

    # Show connection details
    status_text = (
        f"Mobile User Pos: ({x:.1f}, {y:.1f})\n"
        f"Connected BS: "
        f"({serving_bs['x']:.1f}, {serving_bs['y']:.1f})\n"
        f"Active Channel Group: [{serving_bs['freq']}]"
    )

    status_box.set_text(status_text)

    return user_dot, user_path_line, status_box


# Create the animation
anim = FuncAnimation(
    fig,
    update,
    frames=frames_count,
    interval=50,
    blit=True,
    repeat=True
)


# 7. DISPLAY AND FORMATTING
ax.set_title(
    "Cellular Frequency Reuse, Handover & "
    "Interference Simulation",
    fontsize=13,
    fontweight='bold'
)

ax.set_xlim(-12, 17)
ax.set_ylim(-4.5, 6.0)
ax.set_aspect('equal')

ax.grid(True, linestyle=':', alpha=0.5)
ax.legend(loc='upper right', framealpha=0.9)

plt.tight_layout()
plt.show()
