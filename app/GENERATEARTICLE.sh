cd model/grover

PYTHONPATH=$(pwd) python sample/contextual_generate.py -model_config_fn lm/configs/base.json -model_ckpt models/base/model.ckpt -metadata_fn input.json -out_fn output.json