import React from 'react';
import { View, Image, Text } from 'react-native';
import RBButton from '../../Common/RBButton';
import { styles } from './styles';

function FavorFooter({ selectedItems = [] }) {
    return (
        <View style={styles.contrainer}>
            <Text style={styles.text}>{selectedItems.length}개 선택됨</Text>
            <View style={styles.selectedImages}>
                {selectedItems.map((v, i) => (
                    <Image
                        style={[styles.image, { left: i * 20 }]}
                        key={`selected_${v.id}`}
                        source={{ uri: v.image }} />
                ))}
            </View>
            <RBButton style={styles.button} title='선택 완료' />
        </View>
    );
}

export default FavorFooter;