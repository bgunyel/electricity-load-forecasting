import torch
import torch.nn as nn


class GLU(nn.Module):
    """Gated Linear Unit"""

    def __init__(self, in_size: int, out_size: int):
        super().__init__()
        self.linear = nn.Linear(in_size, out_size * 2)
        self.glu = nn.GLU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.linear(x)
        out = self.glu(out)
        return out


class GateAddNorm(nn.Module):
    """Gating & Skip Connection & Layer Norm"""
    def __init__(self, in_size: int, out_size: int):
        super().__init__()
        self.glu = GLU(in_size=in_size, out_size=in_size)
        self.project = nn.Linear(in_size, out_size) if in_size != out_size else nn.Identity()
        self.norm = nn.LayerNorm(out_size)

    def forward(self, x: torch.Tensor, skip_connection: torch.Tensor) -> torch.Tensor:
        out = self.glu(x) + skip_connection
        out = self.project(out)
        out = self.norm(out)
        return x

