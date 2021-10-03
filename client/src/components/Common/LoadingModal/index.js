import React from 'react';
import { Image, Text } from 'react-native';
import OverlayModal from '../OverlayModal';
import { styles } from './styles';

import loadingGif from '../../../../assets/loading.gif'

function LoadingModal({ visible, text, ...props }) {
    return (
        <OverlayModal {...props} visible={visible}>
            <Image style={styles.loading} source={loadingGif} />
            <Text style={styles.text}>{text}</Text>
        </OverlayModal>
    );
}

export default LoadingModal;