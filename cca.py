import argparse
import numpy as np
import cca
import tqdm
import imageio
from util import save_image

parser = argparse.ArgumentParser(description='Cyclic Cellular Automaton simulation')
parser.add_argument('--num_states', type=int, default=5)
parser.add_argument('--random_seed', type=int, default=1, help='random seed')
parser.add_argument('--width', type=int, default=500)
parser.add_argument('--height', type=int, default=500)
parser.add_argument('--range', type=int, default=1)
parser.add_argument('--threshold', type=int, default=1)
parser.add_argument('--num_frames', type=int, default=5)
parser.add_argument('--fname', type=str, default='movie.mp4')

args = parser.parse_args()
np.random.seed(args.random_seed)
M = np.random.randint(0, args.num_states, (args.width, args.height), dtype=int)

with imageio.get_writer(args.fname, mode='I') as writer:
    for i in tqdm.tqdm(range(args.num_frames)):
        M = cca.next_phase(M, args.num_states - 1, args.threshold, args.range)
        fname = save_image(M, i)
        image = imageio.imread(fname)
        writer.append_data(image)



