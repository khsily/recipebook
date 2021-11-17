/*
postman api 문서
@link https://documenter.getpostman.com/view/2590101/UUxzCTjY
*/

import Api from './config';
import * as Category from './models/category';
import * as Ingredient from './models/ingredient';
import * as Recipe from './models/recipe';


export const checkConnection = () => Api.get('test_db');

export {
    Category,
    Ingredient,
    Recipe,
}