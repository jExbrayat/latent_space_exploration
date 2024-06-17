def split_encoder_decoder(encoder_decoder_model):
    # Get encoder layer
    encod = encoder_decoder_model.get_layer(index=0)

    # Get decoder layer
    decod = encoder_decoder_model.get_layer(index=1)

    return encod, decod
