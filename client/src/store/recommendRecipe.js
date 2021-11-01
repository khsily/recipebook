import { makeAutoObservable } from 'mobx';
import { Recipe } from '../api';

class RecipeDetailStore {
    recipes = [];
    page = 0;
    isFetching = false;
    combinationId = [];

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

    async fetchList(page, combinationId, reset) {
        if (this.page >= page) return;
        this._setIsFetching(true);

        this.combinationId = combinationId;

        this._setPage(page);
        let recipes = await Recipe.fetchRecommendList(this.page, combinationId);

        if (reset) recipes = [...recipes.data];
        else recipes = [...this.recipes, ...recipes.data];

        this._setRecipes(recipes);

        this._setIsFetching(false);
    }

    async refresh() {
        await this.fetchList(1, this.combinationId, true);
    }
}

const recipeDetailStore = new RecipeDetailStore();
export default recipeDetailStore;

