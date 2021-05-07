import os
import time
import argparse
import tensorflow as tf
from sampler import WarpSampler
from model import Model
from tqdm import tqdm
from util import *


parser = argparse.ArgumentParser()
parser.add_argument('--dataset', default="Steam3", type=str)
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

args = parser.parse_args()
#if not os.path.isdir(args.dataset + '_' + args.train_dir):
#    os.makedirs(args.dataset + '_' + args.train_dir)
#with open(os.path.join(args.dataset + '_' + args.train_dir, 'args.txt'), 'w') as f:
#    f.write('\n'.join([str(k) + ',' + str(v) for k, v in sorted(vars(args).items(), key=lambda x: x[0])]))
#f.close()


dataset = data_partition(args.dataset)
[user_train, user_valid, user_test, usernum, itemnum] = dataset
num_batch = len(user_train) / args.batch_size


config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.allow_soft_placement = True
sess = tf.Session(config=config)

#sampler = WarpSampler(user_train, usernum, itemnum, batch_size=args.batch_size, maxlen=args.maxlen, n_workers=3)
model = Model(usernum, itemnum, args)

sess.run(tf.initialize_all_variables())


# Added code
checkpoint_path = "checkpoints2/"
saver = tf.train.import_meta_graph('checkpoints2/model.ckpt.meta')
saver.restore(sess, tf.train.latest_checkpoint(checkpoint_path))
print(saver)
#model.summary()


#model.tf_model.load_weights(checkpoint_path)

# Just to run
#for step in tqdm(range(num_batch), total=num_batch, ncols=70, leave=False, unit='b'):
#	u, seq, pos, neg = sampler.next_batch()
        #print(pos)
#        auc, loss, _ = sess.run([model.auc, model.loss, model.train_op],{model.u: u, model.input_seq: seq, model.pos: pos, model.neg: neg,model.is_training: True})



t_test = evaluate(model, dataset, args, sess)
t_valid = evaluate_valid(model, dataset, args, sess)

with open('result.txt', 'w') as f2:
    f2.write('Result: valid (NDCG@10: %.4f, HR@10: %.4f), test (NDCG@10: %.4f, HR@10: %.4f)' % (t_valid[0], t_valid[1], t_test[0], t_test[1]))
#print 'Result: valid (NDCG@10: %.4f, HR@10: %.4f), test (NDCG@10: %.4f, HR@10: %.4f)' % (t_valid[0], t_valid[1], t_test[0], t_test[1])

#f.close()
print("Done")
