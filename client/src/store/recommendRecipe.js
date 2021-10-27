import { makeAutoObservable } from 'mobx';
import { Recipe } from '../api';

class RecipeDetailStore {
    recipes = [];
    page = 0;
    isFetching = false;
    favors = [];

    constructor() {
        makeAutoObservable(this)
    }

    _setPage(page) {
        this.page = page;
    }

    _setRecipes(recipes) {
        this.recipes = recipes;
    }

    _setIsFetching(isFetching) {
        this.isFetching = isFetching;
    }

    reset() {
        this._setPage(0);
        this._setRecipes([]);
    }

    async fetchList(page, favors) {
        this._setIsFetching(true);
        if (this.page >= page) return;

        this.favors = favors;

        this._setPage(page);
        let recipes = await Recipe.fetchRecommendList(this.page);
        recipes = [...this.recipes, ...recipes.data];
        this._setRecipes(recipes);

        this._setIsFetching(false);
    }
}

const recipeDetailStore = new RecipeDetailStore();
export default recipeDetailStore;

