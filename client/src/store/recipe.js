import { makeAutoObservable } from 'mobx';
import { Recipe } from '../api';

class RecipeStore {
    recipes = []
    page = 0;
    isFetching = false;
    favors = [];
    ingredients = [];
    categories = [];

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

    async fetchList({ page, favors, ingredients, categories }, reset) {
        if (this.page >= page) return;
        
        this._setIsFetching(true);


        this.favors = favors;
        this.ingredients = ingredients;
        this.categories = categories;

        this._setPage(page);
        let recipes = await Recipe.searchList({
            page: this.page,
            favors,
            ingredients: ingredients.map(v => v.id),
            categories: categories.map(v => v.id),
        });

        if (reset) recipes = [...recipes.data];
        else recipes = [...this.recipes, ...recipes.data];

        this._setRecipes(recipes);

        this._setIsFetching(false);
    }

    async refresh() {
        if (this.recipes.length === 0) return;

        await this.fetchList({
            page: 1,
            favors: this.favors,
            ingredients: this.ingredients,
            categories: this.categories,
        }, true);
    }
}

const recipeStore = new RecipeStore();
export default recipeStore;

