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
        this.ingredients = await Ingredient.fetchIngredientList();
        this.isFetching = false;
    }
}

const ingredientStore = new IngredientStore();
export default ingredientStore;

