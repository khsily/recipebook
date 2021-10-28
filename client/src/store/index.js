import categoryStore from './category';
import ingredientStore from './ingredient';
import recipeStore from './recipe';
import recommendRecipeStore from './recommendRecipe';
import recipeDetailStore from './recipeDetail';
import favorStore from './favor';
import myFavorStore from './myFavor';
import countStore from './counter';


// 초기 데이터 로드
export async function fetchInitalData() {
    return Promise.all([
        categoryStore.fetchList(),
        ingredientStore.fetchList(),
        myFavorStore.fetchList(),
        favorStore.fetchList(),
    ]);
}


export {
    categoryStore,
    ingredientStore,
    recipeStore,
    recommendRecipeStore,
    recipeDetailStore,
    favorStore,
    myFavorStore,
    countStore,
}