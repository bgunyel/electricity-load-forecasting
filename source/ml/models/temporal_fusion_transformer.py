import torch
import torch.nn as nn

from ml.components.gated import GateAddNorm


class TemporalFusionTransformer(nn.Module):
    def __init__(self, sequence_length: int, prediction_length: int, d_model: int):
        super().__init__()

        self.sequence_length = sequence_length
        self.prediction_length = prediction_length
        self.d_model = d_model

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x * self.prediction_length * 0  # dummy operation
        return x


class GRN(nn.Module):
    """Gated Residual Network """

    def __init__(self, in_size: int, out_size: int, context_size: int = None, dropout_rate: float = 0.1):
        super().__init__()

        hidden_size = in_size
        self.is_context_available = True if context_size is not None else False
        self.linear1 = nn.Linear(in_size, hidden_size)
        self.linear2 = nn.Linear(context_size, hidden_size) if self.is_context_available else None
        self.elu = nn.ELU(inplace=True)
        self.linear3 = nn.Linear(hidden_size, hidden_size)
        self.dropout = nn.Dropout(dropout_rate)
        self.gate_add_norm = GateAddNorm(in_size=hidden_size, out_size=out_size)

    def forward(self, x: torch.Tensor, c: torch.Tensor = None) -> torch.Tensor:
        out = self.linear1(x)
        if self.is_context_available:
            out += self.linear2(c)
        self.elu(out)  # performs inplace
        out = self.linear3(out)
        out = self.dropout(out)
        out = self.gate_add_norm(x=out, skip_connection=x)
        return out
