import torch
import torch.nn as nn
import math

''' copy from ProxyLessNAS '''

class MyModule(nn.Module):

    def forward(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def module_str(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def config(self):
        raise NotImplementedError

    @staticmethod
    def build_from_config(config):
        raise NotImplementedError

    def get_flops(self, *args, **kwargs):
        raise NotImplementedError


class MyNetwork(MyModule):

    def forward(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def module_str(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def config(self):
        raise NotImplementedError

    @staticmethod
    def build_from_config(config):
        raise NotImplementedError

    def get_flops(self, *args, **kwargs):
        raise NotImplementedError

    def set_bn_param(self, momentum, eps):
        for m in self.modules():
            if isinstance(m, nn.BatchNorm2d) or isinstance(m, nn.BatchNorm1d):
                m.momentum = momentum
                m.eps = eps
        return

    def get_bn_param(self):
        for m in self.modules():
            if isinstance(m, nn.BatchNorm2d) or isinstance(m, nn.BatchNorm1d):
                return {
                    'momentum' : m.momentum,
                    'eps': m.eps
                }
        return None

    def init_model(self, model_init, init_div_groups=False):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                if model_init == 'he_fout':
                    n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                    if init_div_groups:
                        n /= m.groups
                    m.weight.data.normal_(0, math.sqrt(2. / n))
                elif model_init == 'he_fin':
                    n = m.kernel_size[0] * m.kernel_size[1] * m.in_channels
                    if init_div_groups:
                        n /= m.groups
                    m.weight.data.normal_(0, math.sqrt(2. / n))
                else:
                    raise NotImplementedError
            elif isinstance(m, nn.BatchNorm2d):
                if m.affine:
                    m.weight.data.fill_(1)
                    m.bias.data.zero_()
                else:
                    continue
            elif isinstance(m, nn.Linear):
                stdv = 1. / math.sqrt(m.weight.size(1))
                m.weight.data.uniform_(-stdv, stdv)
                if m.bias is not None:
                    m.bias.data.zero_()
            elif isinstance(m, nn.BatchNorm1d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    def get_parameters(self, keys=None, mode='include'):

        if keys is None:
            # all the parameters
            for name, param in self.named_parameters():
                yield param
        elif mode == 'include':
            for name, param in self.named_parameters():
                flag = False
                # find parameters have key in name
                for key in keys:
                    if key in name:
                        flag = True
                        break
                if flag:
                    yield param
        elif mode == 'exclude':
            for name, param in self.named_parameters():
                flag = True
                # find parameters do not have key in name
                for key in keys:
                    if key in name:
                        flag = False
                        break
                if flag:
                    yield param
        else:
            raise ValueError('do not support: %s' % mode)

    def weight_parameters(self):
        return self.get_parameters()