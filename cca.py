import argparse
import cca

parser = argparse.ArgumentParser(description='Cyclic Cellular Automaton simulation')
parser.add_argument('--num_states', type=int, default=5)
parser.add_argument('--random_seed', type=int, default=1, help='random seed')
parser.add_argument('--width', type=int, default=500)
parser.add_argument('--height', type=int, default=500)
parser.add_argument('--num_frames', type=int, default=1)

args = parser.parse_args()
np.random.seed(args.random_seed)

M = np.random.randint(0, args.num_states, (args.width, args.height))
for i in range(args.num_frames):
    pass





