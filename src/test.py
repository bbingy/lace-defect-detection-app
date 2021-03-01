from RetinaNet_Pytorch110.inference import inference_single

img_dir = '/home/lby/FaceMask/inference/facemask_lu.jpg'
load_path = '/home/lby/RetinaNet_Pytorch110/checkpoints/retinanet_1e-5/retinanet_15.pth'
save_path = '/home/lby/element-starter/src/static/facemask_lu.jpg'
# inference_batch(img_dir, load_path)
inference_single(img_dir, load_path, save_path)
