import React, { useState } from 'react';
import { Button, Image, Text, View } from 'react-native';
import { observer } from 'mobx-react';
import { counter } from '../../store';
import * as utils from '../../utils'

const HomeScreen = observer(({ navigation }) => {
    const [image, setImage] = useState(null);

    return (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
            <Text>Home Screen</Text>
            <Button title='Go to Search' onPress={() => navigation.navigate('Search')} />

            <Button title={`mobx test ${counter.number}`} onPress={() => counter.increase()} />

            <Button title='open gallery' onPress={async () => {
                result = await utils.open_gallery();
                setImage(result.uri);
                console.log(result);
            }} />

            <Button title='Take Picture' onPress={async () => {
                result = await utils.open_camera();
                setImage(result.uri);
                console.log(result);
            }} />

            {image && <Image source={{ uri: image }} style={{ width: 200, height: 200 }} />}
        </View>
    );
})

export default HomeScreen;
