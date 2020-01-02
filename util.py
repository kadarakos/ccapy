# import matplotlib.pyplot as plt
# import matplotlib
# from pylab import savefig
import random
import numpy as np
from dataclasses import dataclass

import cca


def save_image(image_data, f):
    '''
    image_data is a tensor, in [height width depth]
    image_data is NOT the PIL.Image class
    '''
    plt.subplot(1, 1, 1)
    y_dim = image_data.shape[0]
    x_dim = image_data.shape[1]
    plt.imshow(image_data.reshape(y_dim, x_dim), interpolation='nearest')
    plt.axis('off')

    plt.gca().set_axis_off()
    plt.gca().xaxis.set_major_locator(matplotlib.ticker.NullLocator())
    plt.gca().yaxis.set_major_locator(matplotlib.ticker.NullLocator())
    fname = str(f) + '.png'
    savefig(fname, bbox_inches='tight', pad_inches=0.0)
    return fname

def flip(p):
    return random.random() < p


@dataclass
class CCAInputs:
    width: int
    height: int
    num_states: int
    threshold: int
    range_value: int
    hood: str
    hood_switch_prob: float
    random_seed: int
    color_map: np.array


def cca_rule_str_parser(rule_str: str, args: CCAInputs): 
  if rule_str:
      r, t, s, n = rule_str.split('/')
      args.range_value = int(r)
      args.threshold = int(t)
      args.num_states = int(s) 
      args.hood = 'neumann' if n == 'N' else 'moore'


def generate_cca_frame(states, args: CCAInputs):
    if flip(args.hood_switch_prob):
        args.hood = 'neumann' if args.hood == 'moore' else 'moore'

    states, img = cca.next_phase(states, args.color_map,
                                  args.num_states - 1,
                                  args.threshold, args.range_value,
                                  args.hood)

    img = np.array(img)
    img = img.astype(np.uint8)
    return states, img
