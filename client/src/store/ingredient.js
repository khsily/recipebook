import { makeAutoObservable } from 'mobx';
import { Ingredient } from '../api';

class IngredientStore {
    ingredients = []
    isFetching = false;

    constructor() {
        makeAutoObservable(this)
    }

    async fetchList() {
        this.isFetching = true;
        const ingredients = await Ingredient.fetchIngredientList();
        this.ingredients = ingredients.data;
        this.isFetching = false;
    }
}

const ingredientStore = new IngredientStore();
export default ingredientStore;

