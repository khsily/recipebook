import Api from '../config';

export const fetchIngredientList = () => {
    return Api.get('ingredient');
}