import React from 'react';
import { Text, View, FlatList, ActivityIndicator, Image } from 'react-native';
import { MainTheme } from '../../../styles/themes';

import { styles } from './styles';
import no_result from '../../../../assets/no_result.png';

function RecipeList({ scrollRef, data, renderItem, isFetching, loadMore, search = false }) {
    return (
        <FlatList
            ref={scrollRef}
            style={[styles.listContainer]}
            contentContainerStyle={[styles.listContent]}
            data={data}
            keyExtractor={(item, idx) => `recipe_${search ? 'search' : 'recommend'}_${item.id}_${idx}`}
            onEndReached={loadMore}
            onEndReachedThreshold={2}
            removeClippedSubviews={true}
            legacyImplementation={true}
            ListEmptyComponent={() => (
                <View style={styles.emptyContainer}>
                    {isFetching ?
                        <ActivityIndicator
                            animating={true}
                            size='large'
                            color={MainTheme.colors.primary} />
                        :
                        <>
                            <Image style={styles.emptyImage} source={no_result} />
                            <Text style={styles.emptyText}>레시피가 없어요</Text>
                        </>
                    }
                </View>
            )}
            renderItem={renderItem} />
    );
}

export default RecipeList;