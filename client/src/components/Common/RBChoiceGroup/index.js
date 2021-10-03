import React from 'react';
import { View } from 'react-native';
import RBChoiceChip from '../RBChoiceChip'
import { styles } from './styles';

function RBChoiceGroup({ choices = [], active = 0, onChange = () => { }, ...props }) {
    return (
        <View {...props} style={{ ...styles.container, ...props.style }}>
            {choices.map((v, i) => (
                <RBChoiceChip
                    style={styles.chip}
                    active={active == i}
                    title={v}
                    key={`choice_${i}`}
                    onPress={() => onChange(i)} />
            ))}
        </View>
    );
}

export default RBChoiceGroup;