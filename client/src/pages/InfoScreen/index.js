import React from 'react';
import { View, Text, TouchableOpacity, Linking } from 'react-native';

import { styles } from './styles';

const InfoScreen = () => {
    return (
        <View style={styles.container}>
            <View style={styles.wrapper}>
                <View style={styles.header}>
                    <Text style={styles.title}>Project RecipeBook</Text>
                    <Text style={styles.info}>버전 1.0.0</Text>
                    <Text style={styles.info}>팀 레미 제공</Text>
                </View>

                <View style={styles.contributorContrainer}>
                    <Text style={styles.contributorTitle}>Contributors</Text>
                    <Text style={styles.contributorInfo}>김한수: 앱 / 서버 / DB</Text>
                    <Text style={styles.contributorInfo}>김한성: 추천 모델 (NeuMF) / 데이터수집</Text>
                    <Text style={styles.contributorInfo}>이예인: 객체 인식 모델 (YoloV3) / 데이터수집</Text>
                </View>

                <View style={styles.contributorContrainer}>
                    <Text style={styles.contributorTitle}>Special Thanks</Text>
                    <Text style={styles.contributorInfo}>김희년 멘토님</Text>
                </View>
            </View>

            <TouchableOpacity
                style={styles.button}
                activeOpacity={0.7}
                onPress={() => Linking.openURL(`mailto:hancom.remote@gmail.com`)}>
                <Text style={styles.buttonText}>CONTACT US</Text>
            </TouchableOpacity>
        </View>
    );
}

export default InfoScreen;
