params = {
        'replay_buffer_type': 'priority',
        'replay_buffer_size': 100000,
        'num_episodes': 5000,
        'num_frames': 5000,
        'batch_size': 32,
        'lr': 0.001,
        'gamma': 0.5,
        'rho': 0.25,
        'scheduler_type': 'exponential',
        'e_decay': 10000,
        'e_final': 0.2,
        'hidden_dims': 0,
        'update_frequency': 5,
        'padding_idx': 0,
        'embedding_size': 50,
        'dropout_ratio': 0.2,
        'hidden_size': 100,
        'gat_emb_size': 50,
        'drqa_emb_size': 384,
        'gat_emb_init_file': '',
        'act_emb_init_file': '',
        'preload_weights': False,
        'preload_file': '',
        'pruned': False,
        'max_actions': 40,
        'init_graph_embeds': True,
        'qa_init': False,
        'vocab_size': 1500,
        'cuda_device': 1,
        'gameid': 0,
    }

drqa_params = {
    'doc_hidden_size': 64,
    'doc_layers': 3,
    'doc_dropout_rnn': 0.2,
    'doc_dropout_rnn_output': True,
    'doc_concat_rnn_layers': True,
    'doc_rnn_padding': True
}

params.update(drqa_params)