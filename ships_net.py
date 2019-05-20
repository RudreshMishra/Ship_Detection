import torch
from torch import nn
import torchvision.models as models
import torch.nn.functional as F

class SaveFeatures:
	def __init__(self,layer):
		self.features=None
		self.hook = layer.register_forward_hook(self.hook_fxn)

	def hook_fxn(self,module,input,output):
		self.features = output

	def remove(self):
		self.hook.remove()


class ShipModel(nn.Module):
	def __init__(self):
		super().__init__()
		self.encoder = models.resnet50(pretrained = True)
		self.final_conv = nn.Conv2d(1024,1,kernel_size =1)
		self.layer1_out = SaveFeatures(self.encoder.layer1)
		self.layer2_out = SaveFeatures(self.encoder.layer2)
		self.layer3_out = SaveFeatures(self.encoder.layer3)
		self.layer4_out = SaveFeatures(self.encoder.layer4)

	def forward(self,x):
		x = F.interpolate(x,(224,224))
		self.encoder(x)
		x = self.layer3_out.features
		x = F.interpolate(x,(224,224))
		x = self.final_conv(x)
#		import pdb;pdb.set_trace()
		x = F.interpolate(x,(768,768))
		return x.squeeze()
