import torch
import matplotlib.pyplot as plt
dev = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
a = 50
shots = 10000
U1 = torch.rand(shots, device=dev)
U2 = torch.rand(shots, device=dev)
U3 = torch.rand(shots, device=dev)

rand_r = a * torch.pow(U1, 1 / 3)
rand_t = torch.arccos(1 - 2 * U2)
rand_p = 2 * torch.pi * U3

rand_X = rand_r * torch.sin(rand_t) * torch.cos(rand_p)
rand_Y = rand_r * torch.sin(rand_t) * torch.sin(rand_p)
rand_Z = rand_r * torch.cos(rand_t)

fig = plt.figure(figsize=(8, 8), num="axes")
ax = plt.axes(projection='3d')
ax.scatter3D(rand_X.cpu(), rand_Y.cpu(), rand_Z.cpu(), color='r', alpha=0.1)
plt.show()
