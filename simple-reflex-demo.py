# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import time

# # Define environment parameters
# environment = {
#     "Room1": "Clean",
#     "Room2": "Dirty",
#     "Room3": "Clean",
#     "Room4": "Clean",
    
# }

# room_positions = {
#     "Room1": (0, 0),
#     "Room2": (1, 0),
#     "Room3": (0, 1),
#     "Room4": (1, 1),
# }

# rooms = list(environment.keys())
# agent_index = 0

# def reflex_agent(perception):
#     if perception == "Dirty":
#         return "Clean"
#     else:
#         return "Move"
    

# # Function to visualize the environment
# def visualize_environment(environment, agent_position, step):
#     fig, ax = plt.subplots()
#     for room, status in environment.items():
#         x, y = room_positions[room]
#         color = 'green' if status == "Clean" else 'red'
#         rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
#         ax.add_patch(rect)
#         plt.text(x + 0.5, y + 0.5, room, ha='center', va='center', fontsize=12)
    
#     # Draw the agent
#     agent_x, agent_y = room_positions[rooms[agent_position]]
#     plt.plot(agent_x + 0.5, agent_y + 0.5, 'bo', markersize=10)  # Agent represented as a blue dot
    
#     plt.xlim(-0.5, 2)
#     plt.ylim(-0.5, 2)
#     plt.gca().set_aspect('equal', adjustable='box')
#     plt.title(f"Step {step} - Agent in {rooms[agent_position]}")
    
#     plt.pause(1)
#     plt.close()


# # def draw_environment(environment, agent_position, step):
# #     fig, ax = plt.subplots()
# #     ax.set_xlim(0, 2)
# #     ax.set_ylim(0, 2)
# #     ax.set_xticks([])
# #     ax.set_yticks([])
# #     ax.set_title(f"Step {step} - Agent in {rooms[agent_position]}")
    
# #     for room, status in environment.items():
# #         x, y = room_positions[room]
# #         color = 'green' if status == "Clean" else 'red'
# #         rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
# #         plt.gca().add_patch(rect)
# #         plt.text(x + 0.5, y + 0.5, room, ha='center', va='center', fontsize=12)
    
# #     # Draw the agent
# #     agent_x, agent_y = room_positions[rooms[agent_position]]
# #     plt.plot(agent_x + 0.5, agent_y + 0.5, 'bo', markersize=10)  # Agent represented as a blue dot
    
# #     plt.xlim(-0.5, 2)
# #     plt.ylim(-0.5, 2)
# #     plt.gca().set_aspect('equal', adjustable='box')
# #     plt.title("Vacuum Cleaner Environment")
# #     plt.pause(0.5)

# plt.ion()
# steps = 8

# for step in range(steps):
#     current_room = rooms[agent_index]
#     perception = environment[current_room]
#     action = reflex_agent(perception)
    
#     visualize_environment(environment, agent_index, step+1)
    
#     if action == "Clean":
#         environment[current_room] = "Clean"
#     else:
#         agent_index = (agent_index + 1) % len(rooms)
        

# plt.ioff()

# print("Simulation completed !")


import matplotlib
import importlib.util
import os

if os.environ.get("DISPLAY"):
    if importlib.util.find_spec("tkinter") is not None:
        matplotlib.use("TkAgg")
    elif importlib.util.find_spec("PyQt5") is not None or importlib.util.find_spec("PySide6") is not None:
        matplotlib.use("QtAgg")
    else:
        matplotlib.use("WebAgg")
else:
    matplotlib.use("WebAgg")

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

# Define the 2x2 environment
environment = {
    "Room1": "Clean",
    "Room2": "Dirty",   # Start with dirt here
    "Room3": "Clean",
    "Room4": "Clean"
}

# Mapping for grid positions
room_positions = {
    "Room1": (0, 1),  # Top-left
    "Room2": (1, 1),  # Top-right
    "Room3": (0, 0),  # Bottom-left
    "Room4": (1, 0)   # Bottom-right
}

rooms = list(environment.keys())  
agent_index = 0  

# Reflex Agent Function
def reflex_agent(state):
    if state == "Dirty":
        return "Clean"
    else:
        return "Move"
        
        



#  Function to Draw the Grid
def draw_environment(ax, env, agent_pos, step):
    ax.clear()
    ax.set_xlim(0, 2) 
    ax.set_ylim(0, 2) 
    ax.set_xticks([])
    ax.set_yticks([]) 
    ax.set_title(f"Step {step} — Agent in {rooms[agent_pos]}")

    for room, pos in room_positions.items():  
        x, y = pos
        color = 'red' if env[room] == "Dirty" else 'green'  
        rect = patches.Rectangle((x, y), 1, 1, facecolor=color, edgecolor='black') 
        ax.add_patch(rect)
        ax.text(x + 0.5, y + 0.5, room, ha='center', va='center', color='white', fontsize=10) # "Room1"

    # Draw agent
    agent_x, agent_y = room_positions[rooms[agent_pos]] # Finds the agent's current position.
    agent_patch = patches.Circle((agent_x + 0.5, agent_y + 0.5), 0.1, color='blue') #blue circle
    ax.add_patch(agent_patch)

    plt.draw()
    plt.pause(1)
     
     
     
# Run simulation
plt.ion()
fig, ax = plt.subplots()

steps = 8  


for step in range(steps):
    current_room = rooms[agent_index] 
    state = environment[current_room] 
    action = reflex_agent(state) 

    draw_environment(ax, environment, agent_index, step + 1) 

    if action == "Clean": # If the agent decides to clean, this line updates the environment, marking the room as "Clean".
        environment[current_room] = "Clean"
    else:
        agent_index = (agent_index + 1) % len(rooms) 


plt.ioff() 
plt.show()
print("✅ Simulation complete!") 