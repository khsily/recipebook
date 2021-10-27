import { makeAutoObservable } from 'mobx';
import { Recipe } from '../api';
import { fakeLoading } from '../utils';
import * as dummy from './dummyData';

class RecipeStore {
    recipes = []
    page = 0;
    isFetching = false;

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

    async fetchList({ page, favors, ingredients, categories }) {
        this._setIsFetching(true);

        if (this.page >= page) return;

        this._setPage(page);
        let recipes = await Recipe.searchList({
            page: this.page,
            favors,
            ingredients,
            categories,
        });
        recipes = [...this.recipes, ...recipes.data];
        this._setRecipes(recipes);

        this._setIsFetching(false);
    }
}

const recipeStore = new RecipeStore();
export default recipeStore;

