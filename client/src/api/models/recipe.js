import Api, { objToForm } from '../config';

export const fetchFavorList = () => {
    return Api.get('recipe/favor');
}

export const fetchCombinationId = (favors) => {
    const form = objToForm({ favors });
    return Api.get(`recipe/combination?${form}`);
}