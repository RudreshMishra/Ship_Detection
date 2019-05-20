from ships_net import ShipModel
from ships_dl import get_dl
from torch.optim import Adam
from tqdm import tqdm
from torch.nn import CrossEntropyLoss,BCEWithLogitsLoss

trn_dl = get_dl(True,8)
model = ShipModel().cuda()
# lossfxn = CrossEntropyLoss()
lossfxn = BCEWithLogitsLoss()
optim = Adam(model.parameters())

pbar = tqdm(trn_dl)
for data in pbar:
	optim.zero_grad()
	rgb = data['normalized_rgb']
	preds = model(rgb.cuda())
	loss = lossfxn(preds, data['gt'].type(torch.float).cuda())
	optim.step()
	pbar.set_postfix({'Loss':round(loss.item(),4)})
