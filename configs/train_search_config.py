import argparse
import os

def obtain_train_search_args():
    DEFAULT_PORT =  8097
    DEFAULT_HOSTNAME = 'http://localhost'
    '''
    add_argument(--metavar, type, default, action, choices, help)
    :return: args for train_search phrase
    '''
    parser = argparse.ArgumentParser(description='AutoDeeplab train search configs')

    ''' all need to change '''
    parser.add_argument('--path', type=str, default=os.path.expandvars('$HOME')+'/ljb/Jingbo.TTB/Workspace', help='the path to workspace')
    parser.add_argument('--save_path', type=str, default=os.path.expandvars('$HOME')+'/ljb/WHUBuilding', help='root dir of dataset')
    parser.add_argument('--search_resume', default=False, action='store_true', help='checkpoint file if needed')
    parser.add_argument('--resume_file', type=str, default=None)
    parser.add_argument('--resume_from_warmup', default=False, action='store_true', help='control resume from warmup')

    parser.add_argument('--exp_name', type=str, default='GumbelAutoDeeplab-search')
    parser.add_argument('--gpu_ids', type=int, default=1, help='use single gpu by default')
    parser.add_argument('--random_seed', type=int, default=None)
    parser.add_argument('--open_vis', default=False, action='store_true')

    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--warmup_epochs', type=int, default=20)

    parser.add_argument('--init_lr', type=float, default=0.025)
    parser.add_argument('--warmup_lr', type=float, default=0.05, help='warmup phrase init lr, from origin')
    parser.add_argument('--arch_lr', type=float, default=3e-3, help='Autodeeplab_arch_lr')

    parser.add_argument('--reg_loss_type', type=str, default='add#linear#linearschedule', choices=['add#linear', 'mul#log', 'None', 'add#linear#linearschedule'])
    parser.add_argument('--reg_loss_lambda1', type=float, default=0.006, help='lambda for cell_entropy') # reg param
    parser.add_argument('--reg_loss_lambda2', type=float, default=0.03, help='lambda for arch_entropy')

    parser.add_argument('--train_print_freq', type=int, default=30)
    parser.add_argument('--sample_arch_frequency', type=int, default=1, help='how often sample a new architecture to train operation weight')
    ''' common configs '''


    parser.add_argument('--debug', default=False, action='store_true')
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--search_space', type=str, default='my_search_space', choices=['autodeeplab', 'proxyless', 'counter','my_search_space']) # counter search space is used to debug
    # for visdom

    parser.add_argument('--port', type=int, default=DEFAULT_PORT)
    parser.add_argument('--server', type=str, default=DEFAULT_HOSTNAME)
    parser.add_argument('--compare_phase', default=['train', 'search'])
    # TODO: pay attention to, entropy and warmup loss, iou here
    parser.add_argument('--elements', default=['loss', 'accuracy', 'miou', 'f1score', 'cell_entropy', 'network_entropy', 'entropy', 'warmup_loss', 'warmup_miou'])
    # not used

    #parser.add_argument('--')
    ''' run configs, including network weight training hyperparameters '''

    # data & dataset

    parser.add_argument('--dataset', type=str, default='WHUBuilding', choices=['WHUBuilding'])
    parser.add_argument('--nb_classes', type=int, default=2)
    parser.add_argument('--train_batch_size', type=int, default=16)
    parser.add_argument('--valid_size', type=float, default=None, help='validation set split proportion from training set')
    parser.add_argument('--valid_batch_size', type=int, default=16)
    parser.add_argument('--test_batch_size', type=int, default=6)
    parser.add_argument('--ori_size', type=int, default=512, help='original image size')
    parser.add_argument('--crop_size', type=int, default=512, help='size of cropped patches')
    # optimization
    parser.add_argument('--scheduler', type=str, default='cosine', choices=['multistep', 'cosine', 'exponential', 'linear', 'poly'])
    parser.add_argument('--T_max', type=float, default=None, help='param of cosine') #scheduler param1
    parser.add_argument('--eta_min', type=float, default=0.001, help='param of cosine, min_learning_rate') #scheduler param2
    parser.add_argument('--milestones', type=float, default=None, help='param of multistep') #scheduler param3
    parser.add_argument('--gammas', type=float, default=None, help='param of multistep') #scheduler param4
    parser.add_argument('--gamma', type=float, default=None, help='param of exponential') #scheduler param5
    parser.add_argument('--min_lr', type=float, default=None, help='param of linear') #scheduler param6
    parser.add_argument('--weight_optimizer_type', type=str, default='SGD', choices=['SGD','RMSprop', 'Adam'])
    parser.add_argument('--momentum', type=float, default=0.9) #optim param1
    parser.add_argument('--nesterov', type=bool, default=True) #optim param2
    parser.add_argument('--weight_decay', type=float, default=0.0005) #optim param3

    parser.add_argument('--no_decay_keys', type=str, default=None, choices=[None, 'bn', 'bn#bias'])
    # loss function
    parser.add_argument('--use_unbalanced_weights', default=False, action='store_true')
    parser.add_argument('--criterion', type=str, default='Softmax', choices=['Softmax', 'SmoothSoftmax', 'WeightedSoftmax'])
    parser.add_argument('--label_smoothing', type=float, default=0.)  # criterion param1


    # un-normalized cell_entropy is 4 times larger than arch_entropy.
    # so give cell_entropy a smaller lambda.


    parser.add_argument('--reg_loss_alpha', type=float, default=0.2)  # reg param
    parser.add_argument('--reg_loss_beta', type=float, default=0.3)  # reg param
    # print and save freq
    parser.add_argument('--monitor', type=str, default='max#miou', choices=['max#miou', 'max#fscore'])
    parser.add_argument('--save_ckpt_freq', type=int, default=5)
    parser.add_argument('--validation_freq', type=int, default=1)


    # these two make no sense.
    #parser.add_argument('--print_save_arch_information', default=False, action='store_true')
    #parser.add_argument('--save_normal_net_after_training', default=False, action='store_true')
    #parser.add_argument('--print_arch_param_step_freq', type=int, default=10)
    ''' net configs '''
    parser.add_argument('--nb_layers', type=int, default=12)
    parser.add_argument('--filter_multiplier', type=int, default=32)
    parser.add_argument('--block_multiplier', type=int, default=1)
    parser.add_argument('--steps', type=int, default=1)
    parser.add_argument('--model_init', type=str, default='he_fout', choices=['he_fin', 'he_fout'])
    parser.add_argument('--init_div_groups', default=False, action='store_true')
    parser.add_argument('--bn_momentum', type=float, default=0.1)
    parser.add_argument('--bn_eps', type=float, default=1e-3)
    parser.add_argument('--dropout', type=float, default=0)
    # parser.add_argument('--width_stages', type=str, default='24,40,80,96,192,320')
    # parser.add_argument('--n_cell_stages', type=str, default='4,4,4,4,4,1')
    # parser.add_argument('--stride_stages', type=str, default='2,2,2,1,2,1')
    ''' architecture search config, only using gradient-based algorithm by default '''
    #parser.add_argument('--arch_algo', type=str, default='grad', choices=['grad'])

    #parser.add_argument('--warmup_lr', type=float, default=0.06, help='init_lr of warmup phase, tuned')

    parser.add_argument('--arch_init_type', type=str, default='normal', choices=['normal', 'uniform'])
    parser.add_argument('--arch_init_ratio', type=float, default=1e-3)
    parser.add_argument('--arch_optimizer_type', type=str, default='adam', choices=['sgd', 'adam'])

    # should be 3e-3 or 3e-4
    #parser.add_argument('--arch_lr', type=float, default=3e-4, help='GDAS_arch_lr') # todo, pay attention, change into 3e-3 according to AutoDeeplab
    #parser.add_argument('--arch_lr', type=float, default=4e-3, help='my_tuned_arch_lr')

    parser.add_argument('--arch_adam_beta1', type=float, default=0.5) # arch_optim_param1
    parser.add_argument('--arch_adam_beta2', type=float, default=0.999) # arch_optim_param2
    parser.add_argument('--arch_adam_eps', type=float, default=1e-8) # arch_optim_param3
    parser.add_argument('--arch_weight_decay', type=float, default=1e-3)
    parser.add_argument('--tau_min', type=float, default=0.1, help='the min tau for gumbel')
    parser.add_argument('--tau_max', type=float, default=10, help='the max tau for gumbel')

    # TODO related hardware constraint, None by default
    #parser.add_argument('--target_hardware', type=str, default=None, choices=['mobile', 'cpu', 'gpu8', 'flops', None])


    parser.add_argument('--arch_param_update_frequency', type=int, default=1, help='how often update arch parameters, iterations')
    parser.add_argument('--arch_param_update_steps', type=int, default=1, help='how many times performing update when updating arch_params')
    #parser.add_argument('--grad_binary_mode', type=str, default='full_v2', choices=['full', 'full_v2', 'two'], help='forward and backward mode')
    #parser.add_argument('--grad_data_batch', type=int, default=None, help='batch_size of valid set (from training set)')


    args = parser.parse_args()
    return args

    # TODO not sure configs
    # parser.add_argument('--backbone')
    # related precision parser.add_argument('--opt_level')
    # TODO
    # parser.add_argument('--out_stride')
    # TODO related dataset
    # TODO related parallel training, sync_bn
    # control train or search
    # parser.add_argument('--autodeeplab')

    # cannot resize in segmentation case
    # parser.add_argument('--resize', type=int, default=512)
    # parser.add_argument('--freeze_bn', type=bool, default=False, action='store_true')

    # optimizer parameters
    # parser.add_argument('--min_lr', type=float, default=0.001)


