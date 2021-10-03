import React from 'react';
import { Text, View } from 'react-native';

import { HeaderButton } from '../../components';

import ic_camera from '../../../assets/icon/ic_camera.png';

const SearchScreen = ({ navigation }) => {
    React.useLayoutEffect(() => {
        navigation.setOptions({
            headerRight: () => (
                <HeaderButton icon={ic_camera} onPress={() => alert('camera!!')} />
            )
        });
    }, [navigation]);

    return (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
            <Text>Search Screen</Text>
        </View>
    );
}

export default SearchScreen;
