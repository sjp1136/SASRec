import os
import time
import argparse
import tensorflow as tf
from sampler import WarpSampler
from model import Model
from tqdm import tqdm
from util import *


parser = argparse.ArgumentParser()
parser.add_argument('--dataset', required=True)
parser.add_argument('--train_dir', required=True)
parser.add_argument('--batch_size', default=128, type=int)
parser.add_argument('--lr', default=0.001, type=float)
parser.add_argument('--maxlen', default=50, type=int)
parser.add_argument('--hidden_units', default=50, type=int)
parser.add_argument('--num_blocks', default=2, type=int)
parser.add_argument('--num_epochs', default=201, type=int)
parser.add_argument('--num_heads', default=1, type=int)
parser.add_argument('--dropout_rate', default=0.5, type=float)
parser.add_argument('--l2_emb', default=0.0, type=float)

dataset = data_partition(args.dataset)
[user_train, user_valid, user_test, usernum, itemnum] = dataset

sess = tf.Session(config=config)
model = Model(usernum, itemnum, args)
sess.run(tf.initialize_all_variables())

checkpoint_path = "checkpoints/mode.ckpt"
model.load_weights(checkpoint_path)

t_test = evaluate(model, dataset, args, sess)
t_valid = evaluate_valid(model, dataset, args, sess)
print 'time: %f(s), valid (NDCG@10: %.4f, HR@10: %.4f), test (NDCG@10: %.4f, HR@10: %.4f)' % (T, t_valid[0], t_valid[1], t_test[0], t_test[1])

f.close()
print("Done")
