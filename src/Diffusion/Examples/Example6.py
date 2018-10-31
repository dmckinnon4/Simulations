# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib.animation as animation
# 
# def main():
#     numframes = 100
#     numpoints = 10
#     color_data = np.random.random((numframes, numpoints))
#     x, y, c = np.random.random((3, numpoints))
# 
#     fig = plt.figure()
#     scat = plt.scatter(x, y, c=c, s=100)
# 
#     ani = animation.FuncAnimation(fig, update_plot, frames=range(numframes), fargs=(color_data, scat))
#     plt.show()
# 
# def update_plot(i, data, scat):
#     scat.set_array(data[i])
#     return scat,
# 
# main()
# 
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import numpy as np
# 
# class AnimatedScatter(object):
#     """An animated scatter plot using matplotlib.animations.FuncAnimation."""
#     def __init__(self, numpoints=50):
#         self.numpoints = numpoints
#         self.stream = self.data_stream()
# 
#         # Setup the figure and axes...
#         self.fig, self.ax = plt.subplots()
#         # Then setup FuncAnimation.
#         self.ani = animation.FuncAnimation(self.fig, self.update, interval=5, 
#                                            init_func=self.setup_plot, blit=True)
# 
#     def setup_plot(self):
#         """Initial drawing of the scatter plot."""
#         x, y, s, c = next(self.stream)
#         self.scat = self.ax.scatter(x, y, c=c, s=s, animated=True)
#         self.ax.axis([-10, 10, -10, 10])
# 
#         # For FuncAnimation's sake, we need to return the artist we'll be using
#         # Note that it expects a sequence of artists, thus the trailing comma.
#         return self.scat,
# 
#     def data_stream(self):
#         """Generate a random walk (brownian motion). Data is scaled to produce
#         a soft "flickering" effect."""
#         data = np.random.random((4, self.numpoints))
#         print('data = ', data)
#         xy = data[:2, :]
#         s, c = data[2:, :]
#         xy -= 0.5
#         xy *= 10
#         while True:
#             xy += 0.03 * (np.random.random((2, self.numpoints)) - 0.5)
#             s += 0.05 * (np.random.random(self.numpoints) - 0.5)
#             c += 0.02 * (np.random.random(self.numpoints) - 0.5)
#             yield data
# 
#     def update(self, i):
#         """Update the scatter plot."""
#         data = next(self.stream)
# 
#         # Set x and y data...
# #         self.scat.set_offsets(data[:2, :])
#         self.scat.set_offsets(data[:2, :].reshape(self.numpoints, 2))
#         # Set sizes...
#         self.scat._sizes = 300 * abs(data[2])**1.5 + 100
#         # Set colors..
#         self.scat.set_array(data[3])
# 
#         # We need to return the updated artist for FuncAnimation to draw..
#         # Note that it expects a sequence of artists, thus the trailing comma.
#         return self.scat,
# 
#     def show(self):
#         plt.show()
# 
# if __name__ == '__main__':
#     a = AnimatedScatter(5)
#     a.show()
    
    
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, 1), ax.set_xticks([])
ax.set_ylim(0, 1), ax.set_yticks([])

# Create rain data
n_drops = 50
rain_drops = np.zeros(n_drops, dtype=[('position', float, 2),
                                      ('size',     float, 1),
                                      ('growth',   float, 1),
                                      ('color',    float, 4)])

# Initialize the raindrops in random positions and with
# random growth rates.
rain_drops['position'] = np.random.uniform(0, 1, (n_drops, 2))
rain_drops['growth'] = np.random.uniform(50, 200, n_drops)

# Construct the scatter which we will update during animation
# as the raindrops develop.
scat = ax.scatter(rain_drops['position'][:, 0], rain_drops['position'][:, 1],
                  s=rain_drops['size'], lw=0.5, edgecolors=rain_drops['color'],
                  facecolors='none')


def update(frame_number):
    # Get an index which we can use to re-spawn the oldest raindrop.
    current_index = frame_number % n_drops

    # Make all colors more transparent as time progresses.
    rain_drops['color'][:, 3] -= 1.0/len(rain_drops)
    rain_drops['color'][:, 3] = np.clip(rain_drops['color'][:, 3], 0, 1)

    # Make all circles bigger.
    rain_drops['size'] += rain_drops['growth']

    # Pick a new position for oldest rain drop, resetting its size,
    # color and growth factor.
    rain_drops['position'][current_index] = np.random.uniform(0, 1, 2)
    rain_drops['size'][current_index] = 5
    rain_drops['color'][current_index] = (0, 0, 0, 1)
    rain_drops['growth'][current_index] = np.random.uniform(50, 200)

    # Update the scatter collection, with the new colors, sizes and positions.
    scat.set_edgecolors(rain_drops['color'])
    scat.set_sizes(rain_drops['size'])
    scat.set_offsets(rain_drops['position'])


# Construct the animation, using the update function as the animation
# director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()