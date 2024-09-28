import model.mhformer as mhformer

class Args:
    def __init__(self):
        self.frames = 27
        self.n_joints = 133
        self.channel = 256
        self.layers = 4
        self.d_hid = 512
        self.out_joints = 133

args = Args()

model = mhformer(args)
print(model)