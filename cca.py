import argparse
import numpy as np
import cca
import tqdm
import av
from datetime import datetime
import random

parser = argparse.ArgumentParser(description='Cyclic Cellular Automaton simulation')
parser.add_argument('--rule_str', type=str, default='')
parser.add_argument('--num_states', type=int, default=5)
parser.add_argument('--random_seed', type=int, default=1, help='random seed')
parser.add_argument('--width', type=int, default=500)
parser.add_argument('--height', type=int, default=500)
parser.add_argument('--range', type=int, default=1)
parser.add_argument('--threshold', type=int, default=1)
parser.add_argument('--num_frames', type=int, default=5)
parser.add_argument('--fname', type=str, default='movie.mp4')
parser.add_argument('--hood', type=str, choices=["moore", "neumann"],
                     default='moore')
parser.add_argument('--hood_switch_prob', type=float, default=0)


def flip(p):
    return random.random() < p

args = parser.parse_args()
np.random.seed(args.random_seed)
random.seed(args.random_seed)
if args.rule_str:
    r, t, s, n = args.rule_str.split('/')
    args.range = int(r)
    args.threshold = int(t)
    args.num_states = int(s) 
    args.hood = 'neumann' if n == 'N' else 'moore'

states = np.random.randint(0, args.num_states, (args.width, args.height), dtype=int)

fps = 15
container = av.open(f'test_{datetime.now()}.mp4', mode='w')

stream = container.add_stream('mpeg4', rate=fps)
stream.width = args.width
stream.height = args.height
stream.pix_fmt = 'yuv420p'

color_map = np.array([
    [249,208,137],
    [255,156,91],
    [58,128,130],
    [245,99,74],
    [235,47,59],
])

for i in tqdm.tqdm(range(args.num_frames)):
        if flip(args.hood_switch_prob):
            tmp = args.hood
            args.hood = 'neumann' if tmp == 'moore' else 'moore'

        states, img = cca.next_phase(states, color_map, args.num_states - 1,
                                     args.threshold, args.range,
                                     args.hood)
        img = np.array(img)
        img = img.astype(np.uint8)
    
        frame = av.VideoFrame.from_ndarray(img, format='rgb24')
        for packet in stream.encode(frame):
            container.mux(packet)

# Flush stream
for packet in stream.encode():
    container.mux(packet)

# Close the file
container.close()
