import matplotlib.pyplot as plt
import matplotlib
from pylab import savefig

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
