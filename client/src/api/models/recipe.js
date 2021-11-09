import Api, { objToForm } from '../config';

export const fetchFavorList = () => {
    return Api.get('recipe/favor');
}

export const fetchCombinationId = (favors) => {
    const form = objToForm({ favors });
    return Api.get(`recipe/combination?${form}`);
}

export const fetchRecommendList = (page, combinationId) => {
    const form = objToForm({ combinationId });
    return Api.get(`recipe/recommend/${page}?${form}`);
}

export const searchList = ({ page, ingredients, categories, combinationId }) => {
    return Api.post(`recipe/${page}`, {
        payload: {
            ingredients,
            categories,
            combinationId,
        }
    });
}

export const fetchDetail = (id) => {
    return Api.get(`recipe/${id}`);
}