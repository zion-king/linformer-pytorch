import torch
import torch.nn as nn
import numpy as np

import matplotlib.pyplot as plt

from linformer_pytorch import Linformer

class Visualizer():
    """
    A way to visualize the attention heads for each layer
    """
    def __init__(self, net):
        assert isinstance(net, Linformer), "Only the Linformer is supported"
        self.net = net

    def get_head_visualization(self, depth_no, max_depth, head_no, n_limit, axs):
        """
        Returns the visualization for one head in the Linformer
        """
        curr_mh_attn = self.net.layers[depth_no][0] # First one is mh attn
        curr_head = curr_mh_attn.heads[head_no]

        arr = curr_head.P_bar[0].detach().cpu().numpy()
        assert arr is not None, "Cannot visualize a None matrix!"

        if n_limit is not None:
            arr = arr[:n_limit, :]

        # Remove axis ticks
        axs[depth_no, head_no].set_xticks([])
        axs[depth_no, head_no].set_yticks([])

        pcm = axs[depth_no, head_no].imshow(arr, cmap="Reds", aspect="auto")
        if head_no == 0:
            axs[depth_no, head_no].set_ylabel("Layer {}".format(depth_no+1), fontsize=20)

        if depth_no == max_depth:
            axs[depth_no, head_no].set_xlabel("Head {}".format(head_no+1), fontsize=20)

        return pcm

    def plot_all_heads(self, title="Visualization of Attention Heads", show=True, save_file=None, figsize=(8,6), n_limit=None):
        """
        Showcases all of the heads on a grid. It shows the P_bar matrices for each head,
        which turns out to be an NxK matrix for each of them.
        """

        self.depth = self.net.depth
        self.heads = self.net.nhead

        fig, axs = plt.subplots(self.depth, self.heads, figsize=figsize)
        axs = axs.reshape((self.depth, self.heads)) # In case depth or nheads are 1, bug i think

        fig.suptitle(title, fontsize=26)

        for d_idx in range(self.depth):
            for h_idx in range(self.heads):
                pcm = self.get_head_visualization(d_idx, self.depth-1, h_idx, n_limit, axs)

        if show:
            plt.show()

        if save_file is not None:
            fig.savefig(save_file)
